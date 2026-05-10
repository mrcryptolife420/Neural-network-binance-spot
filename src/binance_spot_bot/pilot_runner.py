from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from .config import BotSettings
from .pilot_orchestrator import PilotRunStore, now_ms
from .redaction import redact_payload
from .runtime import BotRuntime, RuntimeOptions, snapshot_to_dict
from .session_report import export_session_report

RUNNER_ACTIVE_STATES = {"starting", "running", "stopping"}
RUNNER_STALE_MS = 15_000


@dataclass
class PilotRunnerLock:
    runner_id: str
    run_id: str
    pid: int
    status: str
    started_at_ms: int
    updated_at_ms: int
    command_dir: str
    telemetry_jsonl: str
    latest_telemetry_json: str
    process_command: list[str] = field(default_factory=list)
    last_tick_ms: int = 0
    last_reconciliation_ms: int = 0
    last_account_sync_ms: int = 0
    last_command: str = ""
    last_error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class PilotHeartbeatStore:
    def __init__(self, root: Path, stale_ms: int = RUNNER_STALE_MS):
        self.root = root
        self.stale_ms = stale_ms
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock_path = self.root / "runner.lock.json"
        self.runner_path = self.root / "runner.json"

    def write(self, lock: PilotRunnerLock) -> PilotRunnerLock:
        payload = lock.to_dict()
        self.lock_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        self.runner_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return lock

    def read(self) -> PilotRunnerLock | None:
        if not self.lock_path.exists():
            return None
        try:
            return PilotRunnerLock(**json.loads(self.lock_path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, TypeError):
            return None

    def heartbeat_age_ms(self, lock: PilotRunnerLock | None = None) -> int:
        lock = lock or self.read()
        if lock is None:
            return 0
        return max(0, now_ms() - int(lock.updated_at_ms))

    def is_stale(self, lock: PilotRunnerLock | None = None) -> bool:
        lock = lock or self.read()
        if lock is None:
            return False
        return lock.status in RUNNER_ACTIVE_STATES and self.heartbeat_age_ms(lock) > self.stale_ms

    def active_lock(self) -> PilotRunnerLock | None:
        lock = self.read()
        if lock and lock.status in RUNNER_ACTIVE_STATES and not self.is_stale(lock):
            return lock
        return None

    def status_payload(self) -> dict[str, Any]:
        lock = self.read()
        if lock is None:
            return {
                "state": "not_running",
                "alive": False,
                "stale": False,
                "heartbeat_age_ms": 0,
                "next_action": "Start runner",
            }
        stale = self.is_stale(lock)
        state = "stale" if stale else lock.status
        return {
            **lock.to_dict(),
            "state": state,
            "alive": lock.status in RUNNER_ACTIVE_STATES and not stale,
            "stale": stale,
            "heartbeat_age_ms": self.heartbeat_age_ms(lock),
            "next_action": "Resolve stale runner before new start" if stale else "Stop runner" if lock.status == "running" else "Start runner",
        }

    def clear_stale(self) -> bool:
        if not self.is_stale():
            return False
        self.lock_path.unlink(missing_ok=True)
        self.runner_path.unlink(missing_ok=True)
        return True


class PilotCommandQueue:
    def __init__(self, run_root: Path):
        self.root = run_root / "commands"
        self.root.mkdir(parents=True, exist_ok=True)

    def create(self, command_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        created = now_ms()
        command = {
            "command_id": f"{created}-{command_type}",
            "type": command_type,
            "created_at_ms": created,
            "status": "pending",
            "payload": redact_payload(payload or {}),
            "processed_at_ms": 0,
            "result": {},
        }
        self._write(command)
        return command

    def pending(self) -> list[dict[str, Any]]:
        return [item for item in self.all() if item.get("status") == "pending"]

    def all(self) -> list[dict[str, Any]]:
        rows = []
        for path in sorted(self.root.glob("*.json")):
            try:
                rows.append(json.loads(path.read_text(encoding="utf-8")))
            except json.JSONDecodeError:
                continue
        return rows

    def mark(self, command: dict[str, Any], status: str, result: dict[str, Any] | None = None) -> dict[str, Any]:
        command["status"] = status
        command["processed_at_ms"] = now_ms()
        command["result"] = redact_payload(result or {})
        self._write(command)
        return command

    def _write(self, command: dict[str, Any]) -> None:
        path = self.root / f"{command['command_id']}.json"
        path.write_text(json.dumps(redact_payload(command), indent=2, default=str), encoding="utf-8")


class PilotTelemetryStore:
    def __init__(self, run_root: Path):
        self.root = run_root
        self.root.mkdir(parents=True, exist_ok=True)
        self.telemetry_jsonl = self.root / "telemetry.jsonl"
        self.latest_json = self.root / "latest-telemetry.json"

    def append(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = redact_payload({"timestamp_ms": now_ms(), **payload})
        with self.telemetry_jsonl.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, default=str, sort_keys=True) + "\n")
        self.latest_json.write_text(json.dumps(row, indent=2, default=str), encoding="utf-8")
        return row

    def latest(self) -> dict[str, Any]:
        if not self.latest_json.exists():
            return {}
        try:
            return json.loads(self.latest_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def rows(self) -> list[dict[str, Any]]:
        if not self.telemetry_jsonl.exists():
            return []
        rows = []
        for line in self.telemetry_jsonl.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return rows

    def summary(self) -> dict[str, Any]:
        return telemetry_summary(self.rows())


class PilotRunnerService:
    def __init__(
        self,
        settings: BotSettings,
        runtime_factory: Callable[[BotSettings, RuntimeOptions], BotRuntime] = BotRuntime,
        stale_ms: int = RUNNER_STALE_MS,
    ):
        self.settings = settings
        self.root = settings.data_dir / "pilot-runs"
        self.heartbeat = PilotHeartbeatStore(self.root, stale_ms=stale_ms)
        self.run_store = PilotRunStore(self.root)
        self.runtime_factory = runtime_factory

    def status(self) -> dict[str, Any]:
        lock_status = self.heartbeat.status_payload()
        run_id = str(lock_status.get("run_id") or "")
        run_root = self.root / run_id if run_id else self.root
        telemetry_store = PilotTelemetryStore(run_root) if run_id else None
        telemetry = telemetry_store.latest() if telemetry_store else {}
        telemetry_rows = telemetry_store.rows() if telemetry_store else []
        commands = PilotCommandQueue(run_root).all()[-10:] if run_id and run_root.exists() else []
        latest_run = self.run_store.latest()
        status = {
            "runner": lock_status,
            "latest_run": latest_run.to_dict() if latest_run else {},
            "latest_telemetry": telemetry,
            "telemetry_rows": telemetry_rows[-200:],
            "telemetry_summary": telemetry_summary(telemetry_rows),
            "runner_health": runner_health_payload(lock_status, telemetry_rows, commands, latest_run.to_dict() if latest_run else {}),
            "stale_recovery": stale_recovery_payload(lock_status),
            "commands": commands,
            "live_trading_enabled": False,
        }
        return {
            **status,
        }

    def enqueue_command(self, command_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        lock = self.heartbeat.read()
        run_id = lock.run_id if lock else (self.run_store.latest().run_id if self.run_store.latest() else "no-run")
        return PilotCommandQueue(self.root / run_id).create(command_type, payload)

    def clear_stale_lock(self) -> bool:
        return self.heartbeat.clear_stale()

    def run(
        self,
        *,
        symbol: str = "BTCUSDT",
        interval: str = "1m",
        preset: str = "smoke",
        source: str = "demo",
        max_steps: int = 0,
        sleep_seconds: float = 0.0,
    ) -> dict[str, Any]:
        active = self.heartbeat.active_lock()
        if active is not None:
            raise RuntimeError(f"pilot runner already active: {active.runner_id}")
        runtime = self.runtime_factory(
            self.settings,
            RuntimeOptions(
                mode="demo",
                symbol=symbol,
                interval=interval,
                source=source,
                demo_trading_armed=True,
                demo_pilot_preset=preset,
            ),
        )
        initial_snapshot = snapshot_to_dict(runtime.snapshot())
        gate = runtime.pilot_orchestrator.evaluate_start_gate(initial_snapshot, require_not_running=False)
        record = runtime.pilot_orchestrator.prepare_run(initial_snapshot)
        run_root = self.root / record.run_id
        telemetry = PilotTelemetryStore(run_root)
        commands = PilotCommandQueue(run_root)
        lock = PilotRunnerLock(
            runner_id=f"runner-{now_ms()}",
            run_id=record.run_id,
            pid=os.getpid(),
            status="starting",
            started_at_ms=now_ms(),
            updated_at_ms=now_ms(),
            command_dir=str(commands.root),
            telemetry_jsonl=str(telemetry.telemetry_jsonl),
            latest_telemetry_json=str(telemetry.latest_json),
            process_command=sys.argv,
        )
        self.heartbeat.write(lock)
        if not gate["allowed"]:
            lock.status = "resume_required" if gate["state"] == "resume_required" else "failed"
            lock.last_error = gate["next_action"]
            lock.updated_at_ms = now_ms()
            self.heartbeat.write(lock)
            telemetry.append({"runner_status": lock.status, "gate": gate})
            return self.status()
        runtime.start()
        lock.status = "running"
        self._write_runtime_metadata(runtime, lock, telemetry, commands)
        self.heartbeat.write(lock)
        step = 0
        try:
            while max_steps <= 0 or step < max_steps:
                stop_requested = self._process_commands(runtime, lock, telemetry, commands)
                if stop_requested:
                    break
                snapshot = runtime.step()
                step += 1
                self._heartbeat_from_snapshot(lock, snapshot_to_dict(snapshot))
                self.heartbeat.write(lock)
                telemetry.append(self._telemetry_payload(snapshot_to_dict(snapshot), lock))
                self._write_runtime_metadata(runtime, lock, telemetry, commands)
                if snapshot.status in {"completed", "stopped"}:
                    break
                if sleep_seconds:
                    time.sleep(sleep_seconds)
        except Exception as exc:
            lock.status = "failed"
            lock.last_error = str(exc)
            lock.updated_at_ms = now_ms()
            self.heartbeat.write(lock)
            telemetry.append({"runner_status": "failed", "error": str(exc)})
            raise
        finally:
            if lock.status == "running":
                lock.status = "completed"
                lock.updated_at_ms = now_ms()
                self.heartbeat.write(lock)
            if runtime.snapshot().status not in {"completed", "stopped"}:
                runtime.stop()
            self._write_runtime_metadata(runtime, lock, telemetry, commands)
            self._rewrite_report_with_runner(runtime, lock, telemetry, commands)
        return self.status()

    def _process_commands(self, runtime: BotRuntime, lock: PilotRunnerLock, telemetry: PilotTelemetryStore, commands: PilotCommandQueue) -> bool:
        stop_requested = False
        for command in commands.pending():
            command_type = str(command.get("type", ""))
            lock.last_command = command_type
            try:
                if command_type == "stop":
                    lock.status = "stopping"
                    self.heartbeat.write(lock)
                    runtime.stop()
                    commands.mark(command, "processed", {"status": "stopped", "report_paths": runtime.report_paths})
                    stop_requested = True
                elif command_type == "reconcile":
                    commands.mark(command, "processed", runtime.reconcile_demo_orders())
                elif command_type == "cancel_open_orders":
                    commands.mark(command, "processed", {"cancel_status": runtime.cancel_demo_open_orders()})
                elif command_type == "export_report":
                    if runtime.snapshot().status not in {"completed", "stopped"}:
                        runtime.stop()
                    commands.mark(command, "processed", {"report_paths": runtime.report_paths})
                    stop_requested = True
                else:
                    commands.mark(command, "ignored", {"reason": "unsupported command"})
            except Exception as exc:
                lock.last_error = str(exc)
                commands.mark(command, "failed", {"error": str(exc)})
            lock.updated_at_ms = now_ms()
            self.heartbeat.write(lock)
            telemetry.append({"runner_status": lock.status, "last_command": command_type, "command": command})
        return stop_requested

    def _heartbeat_from_snapshot(self, lock: PilotRunnerLock, snapshot: dict[str, Any]) -> None:
        pilot = snapshot.get("demo_pilot", {}) or {}
        lock.updated_at_ms = now_ms()
        lock.last_tick_ms = lock.updated_at_ms
        lock.last_reconciliation_ms = int(pilot.get("last_reconciliation_check_ms") or lock.last_reconciliation_ms or 0)
        lock.last_account_sync_ms = int(pilot.get("last_demo_account_sync_ms") or lock.last_account_sync_ms or 0)

    def _telemetry_payload(self, snapshot: dict[str, Any], lock: PilotRunnerLock) -> dict[str, Any]:
        pilot = snapshot.get("demo_pilot", {}) or {}
        counters = pilot.get("counters", {}) or {}
        return {
            "runner_id": lock.runner_id,
            "run_id": lock.run_id,
            "runner_status": lock.status,
            "heartbeat_age_ms": max(0, now_ms() - int(lock.updated_at_ms)),
            "runtime_status": snapshot.get("status"),
            "pilot_state": (snapshot.get("reconciliation") or {}).get("status", "not-run"),
            "equity": str(snapshot.get("equity", "0")),
            "pnl": str((snapshot.get("metrics") or {}).get("paper_pnl", "0")),
            "orders": counters.get("orders", 0),
            "rejects": counters.get("rejects", 0),
            "api_errors": counters.get("api_errors", 0),
            "reconciliation": snapshot.get("reconciliation", {}),
            "account": snapshot.get("demo_account", {}),
            "open_orders": len(snapshot.get("demo_open_orders", [])),
            "latest_signal": snapshot.get("latest_signal", {}),
            "latest_risk_decision": snapshot.get("latest_risk_decision", {}),
            "latest_execution_result": snapshot.get("latest_execution_result", {}),
            "alerts_count": len(snapshot.get("alerts", [])),
            "report_paths": snapshot.get("report_paths", {}),
        }

    def _write_runtime_metadata(
        self,
        runtime: BotRuntime,
        lock: PilotRunnerLock,
        telemetry: PilotTelemetryStore,
        commands: PilotCommandQueue,
    ) -> None:
        runtime.session.metadata["runner"] = {
            "lock": lock.to_dict(),
            "latest_telemetry": telemetry.latest(),
            "commands": commands.all()[-20:],
        }
        runtime.session_store._write_summary(runtime.session)

    def _rewrite_report_with_runner(
        self,
        runtime: BotRuntime,
        lock: PilotRunnerLock,
        telemetry: PilotTelemetryStore,
        commands: PilotCommandQueue,
    ) -> None:
        self._write_runtime_metadata(runtime, lock, telemetry, commands)
        if runtime.session_finished:
            runtime.report_paths = export_session_report(runtime.session_store, runtime.session.session_id)


def start_background_runner(
    *,
    symbol: str,
    interval: str,
    preset: str,
    source: str = "demo",
    cwd: Path | None = None,
) -> dict[str, Any]:
    command = [
        sys.executable,
        "-m",
        "binance_spot_bot.cli",
        "pilot-runner-start",
        "--foreground",
        "--symbol",
        symbol,
        "--interval",
        interval,
        "--preset",
        preset,
        "--source",
        source,
    ]
    creationflags = 0
    if os.name == "nt":
        creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
    process = subprocess.Popen(command, cwd=str(cwd) if cwd else None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=creationflags)
    return {"pid": process.pid, "command": command, "live_trading_enabled": False}


def telemetry_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "row_count": 0,
            "first_timestamp_ms": 0,
            "last_timestamp_ms": 0,
            "max_heartbeat_age_ms": 0,
            "latest_equity": "0",
            "latest_pnl": "0",
            "latest_runner_status": "not_running",
            "latest_runtime_status": "-",
            "orders": 0,
            "rejects": 0,
            "api_errors": 0,
            "alerts_count": 0,
            "reconciliation_status_counts": {},
        }
    timestamps = [int(row.get("timestamp_ms") or 0) for row in rows]
    latest = rows[-1]
    reconciliation_counts: dict[str, int] = {}
    for row in rows:
        reconciliation = row.get("reconciliation") or {}
        status = str(reconciliation.get("status") or row.get("pilot_state") or "unknown")
        reconciliation_counts[status] = reconciliation_counts.get(status, 0) + 1
    return redact_payload(
        {
            "row_count": len(rows),
            "first_timestamp_ms": min(timestamps) if timestamps else 0,
            "last_timestamp_ms": max(timestamps) if timestamps else 0,
            "max_heartbeat_age_ms": max(int(row.get("heartbeat_age_ms") or 0) for row in rows),
            "latest_equity": str(latest.get("equity", "0")),
            "latest_pnl": str(latest.get("pnl", "0")),
            "latest_runner_status": latest.get("runner_status", "not_running"),
            "latest_runtime_status": latest.get("runtime_status", "-"),
            "orders": int(latest.get("orders") or 0),
            "rejects": int(latest.get("rejects") or 0),
            "api_errors": int(latest.get("api_errors") or 0),
            "alerts_count": int(latest.get("alerts_count") or 0),
            "reconciliation_status_counts": reconciliation_counts,
        }
    )


def command_summary(commands: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    latencies = []
    for command in commands:
        status = str(command.get("status") or "unknown")
        counts[status] = counts.get(status, 0) + 1
        if command.get("processed_at_ms") and command.get("created_at_ms"):
            latencies.append(max(0, int(command["processed_at_ms"]) - int(command["created_at_ms"])))
    return {
        "total": len(commands),
        "pending": counts.get("pending", 0),
        "processed": counts.get("processed", 0),
        "failed": counts.get("failed", 0),
        "ignored": counts.get("ignored", 0),
        "max_latency_ms": max(latencies) if latencies else 0,
    }


def runner_health_payload(
    runner: dict[str, Any],
    telemetry_rows: list[dict[str, Any]],
    commands: list[dict[str, Any]],
    latest_run: dict[str, Any] | None = None,
) -> dict[str, Any]:
    command_stats = command_summary(commands)
    telemetry = telemetry_summary(telemetry_rows)
    report_paths = (latest_run or {}).get("report_paths", {}) if latest_run else {}
    return redact_payload(
        {
            "state": runner.get("state", "not_running"),
            "alive": bool(runner.get("alive", False)),
            "stale": bool(runner.get("stale", False)),
            "heartbeat_age_ms": int(runner.get("heartbeat_age_ms") or 0),
            "run_id": runner.get("run_id", ""),
            "runner_id": runner.get("runner_id", ""),
            "pid": runner.get("pid", "-"),
            "latest_command": runner.get("last_command", ""),
            "pending_commands": command_stats["pending"],
            "failed_commands": command_stats["failed"],
            "ignored_commands": command_stats["ignored"],
            "telemetry_rows": telemetry["row_count"],
            "latest_equity": telemetry["latest_equity"],
            "latest_pnl": telemetry["latest_pnl"],
            "report_paths": len(report_paths),
            "next_safe_action": runner.get("next_action", "Start runner"),
        }
    )


def stale_recovery_payload(runner: dict[str, Any]) -> dict[str, Any]:
    stale = bool(runner.get("stale", False))
    steps = [
        {"step": "Inspect stale state", "status": "required" if stale else "not-needed", "action": "Review heartbeat and latest telemetry"},
        {"step": "Reconcile", "status": "required" if stale else "not-needed", "action": "Send reconcile command"},
        {"step": "Cancel open orders", "status": "conditional", "action": "Only if open/orphan orders remain"},
        {"step": "Export report", "status": "recommended" if stale else "optional", "action": "Preserve runner evidence"},
        {"step": "Clear stale lock", "status": "blocked" if not stale else "available", "action": "Clear only after clean checks"},
        {"step": "Mark resolved", "status": "blocked" if stale else "available", "action": "Use acceptance gate once clean"},
    ]
    return {
        "stale": stale,
        "next_safe_action": "Reconcile stale runner state" if stale else runner.get("next_action", "Start runner"),
        "steps": steps,
    }

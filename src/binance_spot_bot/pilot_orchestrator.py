from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .config import BotSettings
from .demo_pilot import operator_checklist, pipeline_rows
from .exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from .redaction import redact_payload

PILOT_TERMINAL_STATES = {"completed", "failed", "blocked"}
PILOT_STATES = {
    "idle",
    "checking",
    "blocked",
    "ready",
    "running",
    "paused",
    "stopping",
    "completed",
    "failed",
    "resume_required",
}
PILOT_TRANSITIONS = {
    "idle": {"checking", "blocked", "ready", "resume_required"},
    "checking": {"blocked", "ready", "resume_required"},
    "blocked": {"checking", "ready", "resume_required"},
    "ready": {"running", "blocked", "resume_required"},
    "running": {"paused", "stopping", "completed", "failed", "resume_required"},
    "paused": {"running", "stopping", "resume_required"},
    "stopping": {"completed", "failed", "resume_required"},
    "resume_required": {"checking", "ready", "completed"},
    "completed": set(),
    "failed": set(),
}
PILOT_CHECKPOINT_LIMIT = 50
_SNAPSHOT_LIST_KEYS = {
    "audit_tail",
    "candles",
    "signals",
    "fills",
    "equity_points",
    "recent_sessions",
    "order_lifecycle",
    "alerts",
    "demo_open_orders",
    "demo_order_errors",
    "cancel_on_stop_status",
}
_SNAPSHOT_SCALAR_KEYS = {
    "mode",
    "symbol",
    "interval",
    "status",
    "message",
    "session_id",
    "resume_required",
}


def now_ms() -> int:
    return int(time.time() * 1000)


@dataclass(frozen=True)
class PilotGateCheck:
    check: str
    status: str
    reason: str
    next_action: str
    blocking: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PilotRunRecord:
    run_id: str
    state: str
    profile: str
    symbol: str
    preset: str
    started_at_ms: int
    updated_at_ms: int
    completed_at_ms: int | None = None
    blockers: list[dict[str, Any]] = field(default_factory=list)
    transitions: list[dict[str, Any]] = field(default_factory=list)
    checkpoints: list[dict[str, Any]] = field(default_factory=list)
    report_paths: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class PilotRunStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def create_run(self, profile: str, symbol: str, preset: str, state: str, blockers: list[dict[str, Any]] | None = None) -> PilotRunRecord:
        created = now_ms()
        run_id = f"{created}-{symbol.lower()}-{preset}"
        record = PilotRunRecord(
            run_id=run_id,
            state=state,
            profile=profile,
            symbol=symbol,
            preset=preset,
            started_at_ms=created,
            updated_at_ms=created,
            blockers=blockers or [],
            transitions=[{"from": "idle", "to": state, "timestamp_ms": created, "reason": "run created"}],
        )
        self.save(record)
        return record

    def save(self, record: PilotRunRecord) -> PilotRunRecord:
        record.checkpoints = [_compact_checkpoint(item) for item in record.checkpoints[-PILOT_CHECKPOINT_LIMIT:]]
        payload = redact_payload(record.to_dict())
        path = self.path_for(record.run_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        encoded = json.dumps(payload, indent=2, default=str)
        tmp_path = path.with_name("pilot-run.json.tmp")
        try:
            tmp_path.write_text(encoded, encoding="utf-8")
            tmp_path.replace(path)
        except OSError as exc:
            self._write_recovery(record, payload, exc)
        return record

    def load(self, run_id: str) -> PilotRunRecord:
        payload = json.loads(self.path_for(run_id).read_text(encoding="utf-8"))
        return PilotRunRecord(**payload)

    def list_runs(self) -> list[PilotRunRecord]:
        runs = []
        for path in sorted(self.root.glob("*/pilot-run.json")):
            try:
                runs.append(PilotRunRecord(**json.loads(path.read_text(encoding="utf-8"))))
            except (OSError, json.JSONDecodeError, TypeError):
                continue
        return sorted(runs, key=lambda item: item.updated_at_ms, reverse=True)

    def latest(self) -> PilotRunRecord | None:
        runs = self.list_runs()
        return runs[0] if runs else None

    def latest_non_terminal(self) -> PilotRunRecord | None:
        for run in self.list_runs():
            if run.state not in PILOT_TERMINAL_STATES:
                return run
        return None

    def transition(self, run_id: str, to_state: str, reason: str, blockers: list[dict[str, Any]] | None = None) -> PilotRunRecord:
        record = self.load(run_id)
        transition_record(record, to_state, reason, blockers)
        return self.save(record)

    def add_checkpoint(self, run_id: str, event: str, payload: dict[str, Any]) -> PilotRunRecord:
        record = self.load(run_id)
        record.updated_at_ms = now_ms()
        record.checkpoints.append(
            {
                "event": event,
                "timestamp_ms": record.updated_at_ms,
                "payload": redact_payload(_compact_checkpoint_payload(payload)),
            }
        )
        record.checkpoints = record.checkpoints[-PILOT_CHECKPOINT_LIMIT:]
        return self.save(record)

    def attach_report_paths(self, run_id: str, report_paths: dict[str, str]) -> PilotRunRecord:
        record = self.load(run_id)
        record.updated_at_ms = now_ms()
        record.report_paths.update(redact_payload(report_paths))
        return self.save(record)

    def path_for(self, run_id: str) -> Path:
        return self.root / run_id / "pilot-run.json"

    def _write_recovery(self, record: PilotRunRecord, payload: dict[str, Any], exc: OSError) -> None:
        recovery_dir = self.root / "_recovered"
        try:
            recovery_dir.mkdir(parents=True, exist_ok=True)
            recovery_payload = dict(payload)
            recovery_payload["checkpoints"] = recovery_payload.get("checkpoints", [])[-5:]
            recovery_payload["storage_error"] = str(exc)
            recovery_path = recovery_dir / f"{record.run_id}-{now_ms()}.json"
            recovery_path.write_text(json.dumps(redact_payload(recovery_payload), indent=2, default=str), encoding="utf-8")
        except OSError:
            return


def _compact_checkpoint(checkpoint: dict[str, Any]) -> dict[str, Any]:
    compacted = dict(checkpoint)
    payload = compacted.get("payload")
    if isinstance(payload, dict):
        compacted["payload"] = redact_payload(_compact_checkpoint_payload(payload))
    return compacted


def _compact_checkpoint_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"value": _compact_value(payload)}
    if isinstance(payload.get("snapshot"), dict):
        compacted = {key: _compact_value(value) for key, value in payload.items() if key != "snapshot"}
        compacted["snapshot"] = _compact_runtime_snapshot(payload["snapshot"])
        return compacted
    if _looks_like_runtime_snapshot(payload):
        return _compact_runtime_snapshot(payload)
    return _compact_value(payload)


def _looks_like_runtime_snapshot(payload: dict[str, Any]) -> bool:
    return any(key in payload for key in _SNAPSHOT_LIST_KEYS) or {"status", "symbol", "demo_pilot"}.issubset(payload.keys())


def _compact_runtime_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    compacted = {key: snapshot.get(key) for key in _SNAPSHOT_SCALAR_KEYS if key in snapshot}
    for key in (
        "exchange_profile",
        "credential_status",
        "demo_connection",
        "demo_account",
        "reconciliation",
        "demo_pilot",
        "market_data",
        "top_of_book",
        "data_quality",
        "readiness",
        "active_model",
        "paper_account",
        "session_summary",
        "testnet_prechecks",
        "current_candle",
        "latest_signal",
        "latest_risk_decision",
        "latest_execution_result",
        "metrics",
    ):
        if key in snapshot:
            compacted[key] = _compact_value(snapshot.get(key), depth=1)
    for key in _SNAPSHOT_LIST_KEYS:
        if key in snapshot:
            compacted[key] = _compact_list(snapshot.get(key))
    return compacted


def _compact_list(value: Any) -> dict[str, Any]:
    if isinstance(value, dict) and {"count", "latest"}.issubset(value.keys()):
        return value
    rows = list(value or []) if isinstance(value, list) else []
    latest = rows[-1] if rows else None
    return {"count": len(rows), "latest": _compact_value(latest, depth=1) if latest is not None else None}


def _compact_value(value: Any, depth: int = 0) -> Any:
    if depth >= 4:
        return str(value)[:240]
    if isinstance(value, dict):
        return {str(key): _compact_value(item, depth + 1) for key, item in list(value.items())[:40]}
    if isinstance(value, list):
        return _compact_list(value)
    if isinstance(value, tuple):
        return _compact_list(list(value))
    if isinstance(value, str) and len(value) > 500:
        return value[:500] + "...[truncated]"
    return value


def transition_record(
    record: PilotRunRecord,
    to_state: str,
    reason: str,
    blockers: list[dict[str, Any]] | None = None,
) -> PilotRunRecord:
    if to_state not in PILOT_STATES:
        raise ValueError(f"unsupported pilot state: {to_state}")
    allowed = PILOT_TRANSITIONS.get(record.state, set())
    if to_state != record.state and to_state not in allowed:
        raise ValueError(f"invalid pilot transition: {record.state} -> {to_state}")
    timestamp = now_ms()
    record.transitions.append({"from": record.state, "to": to_state, "timestamp_ms": timestamp, "reason": reason})
    record.state = to_state
    record.updated_at_ms = timestamp
    record.blockers = blockers or []
    if to_state in PILOT_TERMINAL_STATES or to_state == "resume_required":
        record.completed_at_ms = timestamp if to_state in PILOT_TERMINAL_STATES else record.completed_at_ms
    return record


def pilot_start_action(record: PilotRunRecord | None, gate: dict[str, Any]) -> dict[str, Any]:
    if record is None:
        return {"allowed": bool(gate.get("allowed")), "action": "start", "next_action": gate.get("next_action", "Start Demo Spot pilot")}
    if record.state == "running":
        return {"allowed": False, "action": "already_running", "next_action": "Pilot is already running"}
    if record.state == "stopping":
        return {"allowed": False, "action": "wait_for_stop", "next_action": "Wait for safe stop to finish"}
    if record.state == "resume_required":
        return {"allowed": False, "action": "recover", "next_action": "Resolve pilot recovery before starting"}
    if not gate.get("allowed"):
        return {"allowed": False, "action": "blocked", "next_action": gate.get("next_action", "Resolve start blockers")}
    return {"allowed": True, "action": "start", "next_action": "Start Demo Spot pilot"}


class DemoPilotOrchestrator:
    def __init__(self, settings: BotSettings, store: PilotRunStore):
        self.settings = settings
        self.store = store
        self.active_run_id: str | None = None

    def evaluate_start_gate(self, snapshot: dict[str, Any], require_not_running: bool = True) -> dict[str, Any]:
        checks = self._start_checks(snapshot, require_not_running=require_not_running)
        blockers = [check.to_dict() for check in checks if check.blocking and check.status == "fail"]
        state = "ready" if not blockers else "resume_required" if _resume_required(snapshot, blockers) else "blocked"
        return {
            "allowed": not blockers,
            "state": state,
            "checks": [check.to_dict() for check in checks],
            "blockers": blockers,
            "next_action": _next_action(blockers),
        }

    def detect_resume(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        latest = self.store.latest_non_terminal()
        open_orders = snapshot.get("demo_open_orders") or []
        reconciliation = snapshot.get("reconciliation", {}) or {}
        needs_resume = bool(latest) or bool(snapshot.get("resume_required")) or bool(open_orders) or bool(reconciliation.get("needs_operator_action"))
        return {
            "resume_required": needs_resume,
            "run_id": latest.run_id if latest else "",
            "state": "resume_required" if needs_resume else "idle",
            "open_orders": len(open_orders),
            "reason": "unfinished pilot/open orders/reconciliation blocker" if needs_resume else "clean",
        }

    def prepare_run(self, snapshot: dict[str, Any]) -> PilotRunRecord:
        gate = self.evaluate_start_gate(snapshot, require_not_running=True)
        profile = str((snapshot.get("exchange_profile") or {}).get("name") or self.settings.exchange_profile)
        symbol = str(snapshot.get("symbol") or "BTCUSDT")
        preset = str(((snapshot.get("demo_pilot") or {}).get("config") or {}).get("pilot_name") or "smoke")
        record = self.store.create_run(profile, symbol, preset, gate["state"], gate["blockers"])
        self.active_run_id = record.run_id
        return record

    def mark_running(self, snapshot: dict[str, Any]) -> PilotRunRecord:
        record = self._ensure_run(snapshot)
        if record.state == "running":
            self.active_run_id = record.run_id
            return self.store.add_checkpoint(record.run_id, "start_idempotent", {"status": "already_running", "snapshot": snapshot})
        if record.state in {"stopping", "resume_required"}:
            blocker = {
                "check": "pilot_state",
                "status": "fail",
                "reason": record.state,
                "next_action": "Wait for safe stop to finish" if record.state == "stopping" else "Resolve pilot recovery before starting",
                "blocking": True,
            }
            transition_record(record, record.state, "start blocked by pilot state", [blocker])
            self.store.save(record)
            self.active_run_id = record.run_id
            return record
        if record.state in PILOT_TERMINAL_STATES:
            self.active_run_id = None
            record = self.prepare_run(snapshot)
        if record.state != "ready":
            gate = self.evaluate_start_gate(snapshot, require_not_running=False)
            transition_record(record, gate["state"], "start gate evaluated", gate["blockers"])
            self.store.save(record)
            if not gate["allowed"]:
                return record
        transition_record(record, "running", "pilot started", [])
        self.store.save(record)
        self.store.add_checkpoint(record.run_id, "start_snapshot", snapshot)
        self.active_run_id = record.run_id
        return record

    def mark_stopping(self) -> PilotRunRecord | None:
        record = self._active_record()
        if record is None:
            return None
        if record.state in {"running", "paused"}:
            return self.store.transition(record.run_id, "stopping", "safe stop requested")
        return record

    def complete_from_snapshot(self, snapshot: dict[str, Any], cancel_status: list[dict[str, Any]] | None = None) -> PilotRunRecord | None:
        record = self._active_record()
        if record is None:
            return None
        state = final_acceptance_state(snapshot, cancel_status or [])
        self.store.add_checkpoint(record.run_id, "stop_snapshot", {"snapshot": snapshot, "cancel_status": cancel_status or []})
        return self.store.transition(record.run_id, state, f"pilot stop flow finished: {state}", self.evaluate_start_gate(snapshot, require_not_running=False)["blockers"])

    def mark_resolved(self, snapshot: dict[str, Any]) -> PilotRunRecord | None:
        record = self._active_record() or self.store.latest_non_terminal()
        if record is None:
            return None
        gate = self.evaluate_start_gate(snapshot, require_not_running=False)
        if gate["allowed"]:
            return self.store.transition(record.run_id, "completed", "operator resolved resume blockers", [])
        return self.store.transition(record.run_id, "resume_required", "resolve attempted but blockers remain", gate["blockers"])

    def attach_report_paths(self, report_paths: dict[str, str]) -> PilotRunRecord | None:
        record = self._active_record()
        if record is None:
            return None
        return self.store.attach_report_paths(record.run_id, report_paths)

    def status_payload(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        gate = self.evaluate_start_gate(snapshot, require_not_running=False)
        resume = self.detect_resume(snapshot)
        latest = self.store.latest()
        active = self._active_record()
        return {
            "state": resume["state"] if resume["resume_required"] else gate["state"],
            "run_id": latest.run_id if latest else "",
            "gate": gate,
            "resume": resume,
            "start_action": pilot_start_action(active, gate),
            "latest_run": latest.to_dict() if latest else {},
            "acceptance": acceptance_summary(snapshot),
        }

    def _ensure_run(self, snapshot: dict[str, Any]) -> PilotRunRecord:
        record = self._active_record()
        if record is not None:
            return record
        return self.prepare_run(snapshot)

    def _active_record(self) -> PilotRunRecord | None:
        if self.active_run_id:
            try:
                return self.store.load(self.active_run_id)
            except FileNotFoundError:
                self.active_run_id = None
        return self.store.latest_non_terminal()

    def _start_checks(self, snapshot: dict[str, Any], require_not_running: bool) -> list[PilotGateCheck]:
        profile = snapshot.get("exchange_profile") or {}
        connection = snapshot.get("demo_connection") or {}
        credentials = snapshot.get("credential_status") or {}
        account = snapshot.get("demo_account") or {}
        reconciliation = snapshot.get("reconciliation") or {}
        prechecks = snapshot.get("testnet_prechecks") or {}
        pilot = snapshot.get("demo_pilot") or {}
        gate_checks = (connection.get("gate") or {}).get("checks") or {}
        open_orders = snapshot.get("demo_open_orders") or []
        status = str(snapshot.get("status") or "unknown")
        profile_name = str(profile.get("name") or connection.get("profile") or self.settings.exchange_profile)
        base_url = str(connection.get("base_url") or self.settings.active_base_url)
        checks = [
            _gate("profile", profile_name == BINANCE_DEMO_SPOT_PROFILE, profile_name, "Select Binance Demo Spot profile"),
            _gate("demo_base_url", "demo-api.binance.com" in base_url, base_url, "Use Demo Spot base URL"),
            _gate("live_disabled", not self.settings.live_trading_enabled, "live disabled" if not self.settings.live_trading_enabled else "live enabled", "Disable live trading"),
            _gate("credentials", bool(credentials.get("has_api_key") and credentials.get("has_api_secret")), credentials.get("capability", "missing"), "Load Demo Spot credentials"),
            _gate("connection", bool(connection.get("connected") or connection.get("authenticated")), (connection.get("gate") or {}).get("reason", "not connected"), "Test connection"),
            _gate("account_can_trade", account.get("status") == "ok" and account.get("can_trade") is True, account.get("error") or account.get("status", "not synced"), "Sync Demo Spot account"),
            _gate("filters_loaded", bool(gate_checks.get("filters_loaded", True)), "symbol filters ready" if gate_checks.get("filters_loaded", True) else "filters missing", "Refresh symbol filters"),
            _gate("risk_limits", bool(prechecks.get("risk_limits_set")), "configured" if prechecks.get("risk_limits_set") else "missing", "Set risk limits"),
            _gate("pilot_preset", bool((pilot.get("config") or {}).get("pilot_name")), (pilot.get("config") or {}).get("pilot_name", ""), "Choose pilot preset"),
            _gate("armed", bool(connection.get("armed")), "armed" if connection.get("armed") else "not armed", "Arm Demo Spot trading"),
            _gate("clean_start", not snapshot.get("resume_required") and not reconciliation.get("needs_operator_action"), reconciliation.get("status", "not-run"), "Reconcile/cancel before start"),
            _gate("no_open_orders", len(open_orders) == 0, f"{len(open_orders)} open orders", "Cancel or reconcile open orders"),
            _gate("runtime_idle", not require_not_running or status not in {"running"}, status, "Stop current runtime"),
        ]
        checks.extend(
            PilotGateCheck(row["check"], row["status"], row["detail"], "Resolve dashboard checklist blocker", row["blocking"])
            for row in operator_checklist(snapshot)
            if row["status"] == "fail" and row["check"] not in {check.check for check in checks}
        )
        return checks


def _gate(check: str, passed: bool, reason: Any, next_action: str, blocking: bool = True) -> PilotGateCheck:
    return PilotGateCheck(check, "pass" if passed else "fail", str(reason or "-"), next_action, blocking)


def _resume_required(snapshot: dict[str, Any], blockers: list[dict[str, Any]]) -> bool:
    names = {item.get("check") for item in blockers}
    return bool(snapshot.get("resume_required")) or bool({"clean_start", "no_open_orders"} & names)


def _next_action(blockers: list[dict[str, Any]]) -> str:
    if not blockers:
        return "Start Demo Spot pilot"
    return str(blockers[0].get("next_action") or "Resolve blockers")


def final_acceptance_state(snapshot: dict[str, Any], cancel_status: list[dict[str, Any]]) -> str:
    reconciliation = snapshot.get("reconciliation") or {}
    open_orders = snapshot.get("demo_open_orders") or []
    cancel_failed = any(item.get("status") == "error" for item in cancel_status)
    if cancel_failed or open_orders or snapshot.get("resume_required") or reconciliation.get("needs_operator_action"):
        return "resume_required"
    if reconciliation.get("failures", 0):
        return "resume_required"
    return "completed"


def acceptance_summary(snapshot: dict[str, Any]) -> dict[str, Any]:
    reconciliation = snapshot.get("reconciliation") or {}
    open_orders = snapshot.get("demo_open_orders") or []
    return {
        "no_open_orders": len(open_orders) == 0,
        "no_orphan_orders": int(reconciliation.get("orphan_orders") or 0) == 0,
        "reconciliation_ok": reconciliation.get("status") in {"ok", "not-run"},
        "resume_required": bool(snapshot.get("resume_required") or reconciliation.get("needs_operator_action")),
    }


def pilot_acceptance_payload(
    summary: Any,
    snapshots: list[dict[str, Any]],
    orders: list[dict[str, Any]],
    alerts: list[dict[str, Any]],
) -> dict[str, Any]:
    latest = snapshots[-1] if snapshots else {}
    cancel_status = latest.get("cancel_on_stop_status") or summary.metadata.get("cancel_on_stop_status", [])
    final_state = final_acceptance_state(latest, cancel_status)
    return redact_payload(
        {
            "run_id": summary.metadata.get("pilot_run", {}).get("run_id", ""),
            "final_acceptance": "accepted" if final_state == "completed" else final_state,
            "session": {
                "session_id": summary.session_id,
                "mode": summary.mode,
                "symbol": summary.symbol,
                "interval": summary.interval,
                "status": summary.status,
                "pnl": str(summary.pnl),
                "max_drawdown": str(summary.max_drawdown),
            },
            "pilot_run": summary.metadata.get("pilot_run", {}),
            "state_transitions": summary.metadata.get("pilot_run", {}).get("transitions", []),
            "runner": summary.metadata.get("runner", {}),
            "start_gate": summary.metadata.get("pilot_start_gate", {}),
            "stop_gate": {
                "cancel_status": cancel_status,
                "final_state": final_state,
                "acceptance": acceptance_summary(latest),
            },
            "operator_checklist": operator_checklist(latest),
            "pipeline": pipeline_rows(latest),
            "account_before_after": {
                "latest_account": latest.get("demo_account", {}),
                "paper_account": latest.get("paper_account", {}),
            },
            "order_lifecycle": latest.get("order_lifecycle", []),
            "reconciliation": latest.get("reconciliation", summary.metadata.get("reconciliation", {})),
            "orders": orders,
            "alerts": alerts,
        }
    )


def pilot_acceptance_markdown(payload: dict[str, Any]) -> str:
    session = payload.get("session", {})
    stop_gate = payload.get("stop_gate", {})
    runner = payload.get("runner", {}) or {}
    runner_lock = runner.get("lock", {}) if isinstance(runner, dict) else {}
    commands = runner.get("commands", []) if isinstance(runner, dict) else []
    return "\n".join(
        [
            f"# Pilot Acceptance {session.get('session_id', '')}",
            "",
            f"- Final acceptance: {payload.get('final_acceptance', '-')}",
            f"- Mode: {session.get('mode', '-')}",
            f"- Symbol: {session.get('symbol', '-')}",
            f"- Status: {session.get('status', '-')}",
            f"- Stop final state: {stop_gate.get('final_state', '-')}",
            f"- Orders: {len(payload.get('orders', []))}",
            f"- Alerts: {len(payload.get('alerts', []))}",
            f"- Runner status: {runner_lock.get('status', '-')}",
            f"- Runner id: {runner_lock.get('runner_id', '-')}",
            "",
            "## Start Gate",
            _markdown_table((payload.get("start_gate") or {}).get("checks", [])),
            "",
            "## Stop Gate",
            _markdown_table([stop_gate.get("acceptance", {})]),
            "",
            "## Operator Checklist",
            _markdown_table(payload.get("operator_checklist", [])),
            "",
            "## Pipeline",
            _markdown_table(payload.get("pipeline", [])),
            "",
            "## Runner",
            _markdown_table(
                [
                    {
                        "runner_id": runner_lock.get("runner_id", ""),
                        "pid": runner_lock.get("pid", ""),
                        "status": runner_lock.get("status", ""),
                        "last_tick_ms": runner_lock.get("last_tick_ms", ""),
                        "last_command": runner_lock.get("last_command", ""),
                    }
                ]
            ),
            "",
            "## Runner Commands",
            _markdown_table(commands[-20:]),
            "",
        ]
    )


def _markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])

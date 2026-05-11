from __future__ import annotations

import importlib.metadata
import json
import platform
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .config import BotSettings
from .pilot_orchestrator import PILOT_TERMINAL_STATES
from .redaction import redact_payload


FRESHNESS_SECONDS = 24 * 60 * 60
RUNNER_STALE_SECONDS = 5 * 60


@dataclass(frozen=True)
class DiagnosticsReport:
    status: str
    blockers: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[dict[str, Any]] = field(default_factory=list)
    next_safe_action: str = ""
    python: str = ""
    platform: str = ""
    data_dir: str = ""
    audit_log_path: str = ""
    pkgs: dict[str, str] = field(default_factory=dict)
    live_trading_enabled: bool = False
    artifact_inventory: list[dict[str, Any]] = field(default_factory=list)
    pilot_run_health: dict[str, Any] = field(default_factory=dict)
    runner_lock_health: dict[str, Any] = field(default_factory=dict)
    recommended_actions: list[dict[str, str]] = field(default_factory=list)
    generated_at_ms: int = 0

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class OperatorDiagnostics:
    def __init__(self, settings: BotSettings, project_root: Path | None = None) -> None:
        self.settings = settings
        self.project_root = project_root or Path.cwd()
        self.data_dir = Path(settings.data_dir)

    def state_health(self) -> DiagnosticsReport:
        blockers: list[dict[str, Any]] = []
        warnings: list[dict[str, Any]] = []
        inventory = self.artifact_health()
        pilot_health = self.pilot_run_health()
        runner_health = self.runner_lock_health()

        if self.settings.live_trading_enabled:
            blockers.append(_finding("live_trading_enabled", "live trading is enabled", "Disable live trading"))
        for item in inventory:
            if item["state"] == "invalid_json":
                warnings.append(_finding(f"{item['name']}.invalid_json", "artifact is invalid JSON", "Regenerate artifact", item["path"]))
            elif item["state"] == "missing" and item.get("critical"):
                warnings.append(_finding(f"{item['name']}.missing", "critical evidence artifact missing", "Run rehearsal or check-all", item["path"]))
            elif item["state"] == "stale":
                warnings.append(_finding(f"{item['name']}.stale", "artifact is stale", "Refresh evidence", item["path"]))

        if pilot_health.get("state") in {"running", "stopping", "resume_required"} and pilot_health.get("stale"):
            warnings.append(_finding("pilot_run.stale_non_terminal", "pilot run is non-terminal and stale", "Open Recovery & Diagnostics"))
        if runner_health.get("state") == "stale":
            warnings.append(_finding("runner_lock.stale", "runner lock is stale", "Verify no runner process is active"))
        if runner_health.get("failed_commands", 0):
            blockers.append(_finding("runner.failed_commands", "runner has failed commands", "Review runner telemetry"))

        status = "fail" if blockers else "warn" if warnings else "ok"
        actions = self.recommended_actions(blockers, warnings)
        return DiagnosticsReport(
            status=status,
            blockers=blockers,
            warnings=warnings,
            next_safe_action=actions[0]["action"] if actions else "No recovery action required.",
            python=sys.version.split()[0],
            platform=platform.platform(),
            data_dir=str(self.data_dir),
            audit_log_path=str(Path(self.settings.audit_log_path)),
            pkgs=_package_versions(),
            live_trading_enabled=False,
            artifact_inventory=inventory,
            pilot_run_health=pilot_health,
            runner_lock_health=runner_health,
            recommended_actions=actions,
            generated_at_ms=_now_ms(),
        )

    def artifact_health(self) -> list[dict[str, Any]]:
        specs = [
            ("launch_evidence", self.data_dir / "checks" / "dashboard" / "launch-evidence.json", True),
            ("browser_smoke", self.data_dir / "checks" / "dashboard" / "browser-smoke.json", False),
            ("check_all", self.data_dir / "checks" / "check-all.json", True),
            ("demo_execution", self.data_dir / "evidence" / "demo-execution" / "demo_execution_drill.json", True),
            ("pilot_start_idempotency", self.data_dir / "evidence" / "pilot-start-idempotency.json", True),
            ("scorecard", self.data_dir / "evidence" / "scorecards" / "latest-scorecard.json", False),
            ("rehearsal", self.data_dir / "evidence" / "rehearsals" / "latest.json", False),
        ]
        operator = _latest_file(self.data_dir / "evidence" / "dashboard", "operator-evidence-*.json")
        specs.append(("operator_evidence", operator or self.data_dir / "evidence" / "dashboard", True))
        return [self._artifact_item(name, path, critical) for name, path, critical in specs]

    def pilot_run_health(self) -> dict[str, Any]:
        runs = _read_json_files(self.data_dir / "pilot-runs", "*/pilot-run.json")
        runs.sort(key=lambda row: int(row.get("updated_at_ms") or row.get("started_at_ms") or 0), reverse=True)
        latest = runs[0] if runs else {}
        state = str(latest.get("state") or "none")
        updated = int(latest.get("updated_at_ms") or 0)
        age = max(0, int(time.time()) - int(updated / 1000)) if updated else 0
        non_terminal = [row for row in runs if str(row.get("state")) not in PILOT_TERMINAL_STATES]
        return redact_payload(
            {
                "state": state,
                "run_id": latest.get("run_id", ""),
                "age_seconds": age,
                "stale": bool(state in {"running", "stopping", "resume_required"} and age > RUNNER_STALE_SECONDS),
                "non_terminal_count": len(non_terminal),
                "recent": runs[:5],
            }
        )

    def runner_lock_health(self) -> dict[str, Any]:
        lock_path = self.data_dir / "pilot-runs" / "runner.lock.json"
        payload, state = _load_json_state(lock_path)
        updated = int(payload.get("updated_at_ms") or 0) if isinstance(payload, dict) else 0
        age = max(0, int(time.time()) - int(updated / 1000)) if updated else 0
        stale = bool(lock_path.exists() and (state != "fresh" or not updated or age > RUNNER_STALE_SECONDS))
        return redact_payload(
            {
                "state": "stale" if stale else "active" if lock_path.exists() else "missing",
                "path": str(lock_path),
                "age_seconds": age,
                "runner_id": payload.get("runner_id", "") if isinstance(payload, dict) else "",
                "run_id": payload.get("run_id", "") if isinstance(payload, dict) else "",
                "failed_commands": int(payload.get("failed_commands", 0) or 0) if isinstance(payload, dict) else 0,
            }
        )

    def recommended_actions(self, blockers: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> list[dict[str, str]]:
        findings = blockers + warnings
        if not findings:
            return [{"severity": "info", "action": "No recovery action required."}]
        return [{"severity": str(item.get("severity", "warning")), "action": str(item.get("next_action", "Review diagnostics")), "source": str(item.get("name", ""))} for item in findings]

    def write_health_report(self) -> Path:
        path = self.data_dir / "evidence" / "diagnostics" / "latest-diagnostics.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = self.state_health().to_dict()
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        self.append_history(payload)
        return path

    def append_history(self, payload: dict[str, Any] | None = None) -> Path:
        history = self.data_dir / "evidence" / "diagnostics" / "history.jsonl"
        history.parent.mkdir(parents=True, exist_ok=True)
        row = payload or self.state_health().to_dict()
        with history.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(redact_payload(row), default=str) + "\n")
        return history

    def trend_summary(self, limit: int = 50) -> dict[str, Any]:
        history = self.data_dir / "evidence" / "diagnostics" / "history.jsonl"
        rows: list[dict[str, Any]] = []
        if history.exists():
            for line in history.read_text(encoding="utf-8").splitlines():
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(payload, dict):
                    rows.append(payload)
        rows = rows[-limit:]
        statuses = [str(row.get("status", "unknown")) for row in rows]
        latest = rows[-1] if rows else {}
        return redact_payload(
            {
                "status": latest.get("status", "unknown") if latest else "empty",
                "points": len(rows),
                "ok": statuses.count("ok"),
                "warn": statuses.count("warn"),
                "fail": statuses.count("fail"),
                "latest_blockers": len(latest.get("blockers", [])) if latest else 0,
                "latest_warnings": len(latest.get("warnings", [])) if latest else 0,
                "live_trading_enabled": False,
            }
        )

    def _artifact_item(self, name: str, path: Path, critical: bool) -> dict[str, Any]:
        payload, state = _load_json_state(path)
        updated = int(path.stat().st_mtime) if path.is_file() else 0
        age = max(0, int(time.time()) - updated) if updated else 0
        if state == "fresh" and age > FRESHNESS_SECONDS:
            state = "stale"
        return redact_payload(
            {
                "name": name,
                "path": str(path),
                "critical": critical,
                "exists": path.is_file(),
                "state": state,
                "age_seconds": age,
                "status": payload.get("status", "") if isinstance(payload, dict) else "",
            }
        )


def collect_diagnostics(settings: BotSettings) -> DiagnosticsReport:
    return OperatorDiagnostics(settings).state_health()


def write_diagnostics_report(settings: BotSettings, project_root: Path | None = None) -> Path:
    return OperatorDiagnostics(settings, project_root).write_health_report()


def _package_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for pkg in ("streamlit", "plotly", "pytest"):
        try:
            versions[pkg] = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            versions[pkg] = "missing"
    return versions


def _artifact_state(path: Path) -> str:
    if not path.exists():
        return "missing"
    if not path.is_file():
        return "missing"
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "invalid_json"
    except OSError:
        return "unreadable"
    return "fresh"


def _load_json_state(path: Path) -> tuple[dict[str, Any], str]:
    state = _artifact_state(path)
    if state != "fresh":
        return {}, state
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}, "invalid_json"
    return payload if isinstance(payload, dict) else {"value": payload}, state


def _latest_file(root: Path, pattern: str) -> Path | None:
    try:
        files = sorted(root.glob(pattern), key=lambda item: item.stat().st_mtime)
    except OSError:
        return None
    return files[-1] if files else None


def _read_json_files(root: Path, pattern: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not root.exists():
        return rows
    for path in root.glob(pattern):
        payload, state = _load_json_state(path)
        if state == "fresh":
            rows.append(payload)
    return rows


def _finding(name: str, message: str, next_action: str, path: str = "", severity: str = "warning") -> dict[str, str]:
    return {"severity": severity, "name": name, "message": message, "next_action": next_action, "path": path}


def _now_ms() -> int:
    return int(time.time() * 1000)

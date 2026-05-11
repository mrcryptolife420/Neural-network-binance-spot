from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import BotSettings
from .pilot_runner import PilotRunnerService
from .redaction import redact_payload


@dataclass(frozen=True)
class ScorecardItem:
    severity: str
    name: str
    message: str
    path: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceScorecard:
    status: str
    blockers: list[ScorecardItem] = field(default_factory=list)
    warnings: list[ScorecardItem] = field(default_factory=list)
    artifacts: dict[str, str] = field(default_factory=dict)
    next_safe_action: str = ""
    live_trading_enabled: bool = False
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(
            {
                "status": self.status,
                "blockers": [item.to_dict() for item in self.blockers],
                "warnings": [item.to_dict() for item in self.warnings],
                "artifacts": self.artifacts,
                "next_safe_action": self.next_safe_action,
                "live_trading_enabled": False,
                "generated_at": self.generated_at,
            }
        )


def generate_evidence_scorecard(settings: BotSettings, *, write: bool = True) -> EvidenceScorecard:
    data_dir = settings.data_dir
    blockers: list[ScorecardItem] = []
    warnings: list[ScorecardItem] = []
    artifacts: dict[str, str] = {}

    launch = _load_artifact(data_dir / "checks" / "dashboard" / "launch-evidence.json", "launch_evidence", artifacts, warnings)
    browser = _load_artifact(data_dir / "checks" / "dashboard" / "browser-smoke.json", "browser_smoke", artifacts, warnings)
    operator = _load_latest_operator_evidence(data_dir, artifacts, warnings)
    demo_execution = _load_artifact(data_dir / "evidence" / "demo-execution" / "demo_execution_drill.json", "demo_execution", artifacts, warnings)
    pilot_start_idempotency = _load_artifact(data_dir / "evidence" / "pilot-start-idempotency.json", "pilot_start_idempotency", artifacts, warnings)
    diagnostics = _load_artifact(data_dir / "evidence" / "diagnostics" / "latest-diagnostics.json", "operator_diagnostics", artifacts, warnings)

    for name, payload in (
        ("launch_evidence", launch),
        ("browser_smoke", browser),
        ("operator_evidence", operator),
        ("demo_execution", demo_execution),
        ("pilot_start_idempotency", pilot_start_idempotency),
        ("operator_diagnostics", diagnostics),
    ):
        if payload and _contains_live_enabled(payload):
            blockers.append(ScorecardItem("blocker", f"{name}.live_enabled", "live trading enabled in evidence", artifacts.get(name, "")))

    if browser and browser.get("status") != "ok":
        blockers.append(ScorecardItem("blocker", "browser_smoke.failed", "dashboard browser smoke is not ok", artifacts.get("browser_smoke", "")))

    if demo_execution:
        status = str(demo_execution.get("status", "")).upper()
        if status in {"UNKNOWN", "RECONCILE_NEEDED"}:
            blockers.append(ScorecardItem("blocker", "demo_execution.reconcile_needed", f"demo execution status is {status}", artifacts.get("demo_execution", "")))
        for row in demo_execution.get("lifecycle", []) or []:
            if row.get("needs_reconciliation"):
                blockers.append(ScorecardItem("blocker", "demo_execution.lifecycle_reconcile_needed", "order lifecycle needs reconciliation", artifacts.get("demo_execution", "")))
                break

    if pilot_start_idempotency:
        if pilot_start_idempotency.get("status") != "ok":
            blockers.append(ScorecardItem("blocker", "pilot_start_idempotency.failed", "pilot double-start idempotency failed", artifacts.get("pilot_start_idempotency", "")))
        if pilot_start_idempotency.get("invalid_running_to_ready_transition"):
            blockers.append(ScorecardItem("blocker", "pilot_start_idempotency.invalid_transition", "running to ready transition detected", artifacts.get("pilot_start_idempotency", "")))
    if diagnostics:
        if diagnostics.get("status") == "fail":
            blockers.append(ScorecardItem("blocker", "operator_diagnostics.failed", "operator diagnostics has blockers", artifacts.get("operator_diagnostics", "")))
        elif diagnostics.get("status") == "warn":
            warnings.append(ScorecardItem("warning", "operator_diagnostics.warn", "operator diagnostics has warnings", artifacts.get("operator_diagnostics", "")))

    runner_status = PilotRunnerService(settings).status()
    runner = runner_status.get("runner", {})
    runner_health = runner_status.get("runner_health", {})
    if runner.get("stale"):
        blockers.append(ScorecardItem("blocker", "runner.stale", "pilot runner is stale"))
    if int(runner_health.get("failed_commands", 0) or 0) > 0:
        blockers.append(ScorecardItem("blocker", "runner.failed_commands", "runner has failed commands"))
    if runner.get("alive") and not runner_status.get("telemetry_rows"):
        warnings.append(ScorecardItem("warning", "runner.telemetry_missing", "no runner telemetry rows found"))

    if not (data_dir / "checks" / "check-all.json").exists():
        warnings.append(ScorecardItem("warning", "check_all.missing", "no saved check-all artifact found"))

    status = "fail" if blockers else "warn" if warnings else "pass"
    next_action = _next_action(status, blockers, warnings)
    scorecard = EvidenceScorecard(status, blockers, warnings, artifacts, next_action, live_trading_enabled=False)
    if write:
        write_scorecard(settings, scorecard)
    return scorecard


def write_scorecard(settings: BotSettings, scorecard: EvidenceScorecard) -> Path:
    out_dir = settings.data_dir / "evidence" / "scorecards"
    out_dir.mkdir(parents=True, exist_ok=True)
    latest = out_dir / "latest-scorecard.json"
    stamped = out_dir / f"scorecard-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    payload = json.dumps(scorecard.to_dict(), indent=2, default=str)
    latest.write_text(payload, encoding="utf-8")
    stamped.write_text(payload, encoding="utf-8")
    return latest


def _load_artifact(path: Path, name: str, artifacts: dict[str, str], warnings: list[ScorecardItem]) -> dict[str, Any]:
    if not path.exists():
        warnings.append(ScorecardItem("warning", f"{name}.missing", "artifact missing", str(path)))
        return {}
    artifacts[name] = str(path)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        warnings.append(ScorecardItem("warning", f"{name}.invalid_json", "artifact is invalid JSON", str(path)))
        return {}


def _load_latest_operator_evidence(data_dir: Path, artifacts: dict[str, str], warnings: list[ScorecardItem]) -> dict[str, Any]:
    files = sorted((data_dir / "evidence" / "dashboard").glob("operator-evidence-*.json"))
    if not files:
        warnings.append(ScorecardItem("warning", "operator_evidence.missing", "artifact missing", str(data_dir / "evidence" / "dashboard")))
        return {}
    return _load_artifact(files[-1], "operator_evidence", artifacts, warnings)


def _contains_live_enabled(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "live_trading_enabled" and item is True:
                return True
            if _contains_live_enabled(item):
                return True
    if isinstance(value, list):
        return any(_contains_live_enabled(item) for item in value)
    return False


def _next_action(status: str, blockers: list[ScorecardItem], warnings: list[ScorecardItem]) -> str:
    if status == "fail":
        return f"Resolve blocker: {blockers[0].message}"
    if status == "warn":
        return f"Collect or refresh evidence: {warnings[0].message}"
    return "Evidence gates pass; continue demo/paper operations only."

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import has_advice_wording, json_write, now_ms, redact_value, stable_hash, to_plain

from . import LOCAL_ONLY_STATEMENT, NO_LIVE_ORDER_STATEMENT, SAFE_ENV

VALID_PHASES = {"start", "runtime", "finish", "crash", "collect", "export"}
VALID_STATUSES = {"running", "ok", "warning", "failed", "crashed", "blocked"}


@dataclass
class AIDoctorArtifactRef:
    artifact_id: str
    path: str
    sha256: str = ""


@dataclass
class AIDoctorFinding:
    finding_id: str
    title: str
    severity: str
    evidence_refs: list[str] = field(default_factory=list)
    suspect_files: list[str] = field(default_factory=list)


@dataclass
class AIDoctorStartSnapshot:
    run_id: str
    started_at_ms: int
    project_root: str
    python_version: str
    platform: str
    safe_env: dict[str, str]


@dataclass
class AIDoctorFinishSnapshot:
    run_id: str
    finished_at_ms: int
    status: str
    exit_code: int | None = None
    next_safe_action: str = "export_ai_doctor_bundle"


@dataclass
class AIDoctorRun:
    run_id: str
    profile_id: str
    mode: str
    app_entrypoint: str
    started_at_ms: int
    status: str = "running"
    phase: str = "start"
    finished_at_ms: int | None = None
    exit_code: int | None = None
    error_count: int = 0
    warning_count: int = 0
    blocker_count: int = 0
    dashboard_url: str = ""
    data_dir: str = "data"
    project_root: str = "."
    git_ref: str = "local"
    python_version: str = field(default_factory=lambda: sys.version.split()[0])
    platform: str = field(default_factory=platform.platform)
    safe_env: dict[str, str] = field(default_factory=lambda: dict(SAFE_ENV))
    live_trading_enabled: bool = False
    kill_switch: bool = True
    artifacts: list[AIDoctorArtifactRef] = field(default_factory=list)
    no_live_order_statement: str = NO_LIVE_ORDER_STATEMENT
    local_only_statement: str = LOCAL_ONLY_STATEMENT
    secret_redaction_status: str = "redacted"


@dataclass
class AIDoctorRunReport:
    status: str
    run: AIDoctorRun
    findings: list[AIDoctorFinding] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def create_ai_doctor_run_id(profile_id: str = "default", seed: str = "") -> str:
    return "ai-doctor-" + stable_hash({"profile": profile_id, "seed": seed, "time": now_ms()})[:16]


def validate_ai_doctor_run(run: AIDoctorRun) -> tuple[list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []
    if run.live_trading_enabled:
        blockers.append("live_trading_enabled must be false")
    if run.safe_env.get("LIVE_TRADING_ENABLED") != "false":
        blockers.append("safe env missing LIVE_TRADING_ENABLED=false")
    if run.safe_env.get("KILL_SWITCH") != "true":
        blockers.append("safe env missing KILL_SWITCH=true")
    if run.no_live_order_statement != NO_LIVE_ORDER_STATEMENT:
        blockers.append("no live order statement missing")
    if not run.secret_redaction_status:
        blockers.append("secret redaction status missing")
    if run.status not in VALID_STATUSES:
        blockers.append("invalid status")
    if run.phase not in VALID_PHASES:
        blockers.append("invalid phase")
    if run.dashboard_url and not run.dashboard_url.startswith(("http://127.0.0.1", "http://localhost")):
        blockers.append("unsafe dashboard_url")
    if has_advice_wording(run):
        blockers.append("advice wording blocked")
    return blockers, warnings


def redact_ai_doctor_payload(payload: Any) -> Any:
    return redact_value(to_plain(payload))


def ai_doctor_run_to_dict(run: AIDoctorRun) -> dict[str, Any]:
    blockers, warnings = validate_ai_doctor_run(run)
    payload = redact_ai_doctor_payload(run)
    payload["validation_status"] = "blocked" if blockers else "ok"
    payload["blockers"] = blockers
    payload["warnings"] = warnings
    return payload


def write_ai_doctor_run_report(root: Path, report: AIDoctorRunReport) -> dict[str, Any]:
    return json_write(root / "data" / "ai-doctor" / "runs" / report.run.run_id / "run_report.json", report)


def create_default_run(root: Path, profile_id: str = "paper", mode: str = "safe") -> AIDoctorRun:
    return AIDoctorRun(
        run_id=create_ai_doctor_run_id(profile_id, str(root)),
        profile_id=profile_id,
        mode=mode,
        app_entrypoint="dashboard-v2",
        started_at_ms=now_ms(),
        project_root=str(root),
        data_dir=str(root / "data"),
    )


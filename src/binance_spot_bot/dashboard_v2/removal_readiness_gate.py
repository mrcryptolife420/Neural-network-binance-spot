from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .deprecation_gate import dashboard_v2_deprecation_gate
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


@dataclass(frozen=True)
class StreamlitRemovalGateInput:
    deprecation_gate: str = "deprecation_candidate"
    v2_only_smoke: str = "ok"
    browser_smoke: str = "ok"
    api_smoke: str = "ok"
    uat_open_p0_p1: int = 0
    critical_parity_missing: int = 0
    support_evidence: str = "ok"
    rollback_archive_present: bool = False
    streamlit_imported_by_v2: bool = False
    docs_v2_only: bool = True
    check_all_v2_only: str = "ok"
    no_live_proof: str = field(default_factory=dashboard_v2_no_live_statement)
    live_mode_found: bool = False


@dataclass(frozen=True)
class StreamlitRemovalBlocker:
    code: str
    severity: str
    message: str


@dataclass(frozen=True)
class StreamlitRemovalReadinessDecision:
    outcome: str
    remove_code_now: bool
    keep_legacy: bool
    explanation: str


@dataclass(frozen=True)
class StreamlitRemovalReadinessReport:
    status: str
    decision: StreamlitRemovalReadinessDecision
    blockers: list[StreamlitRemovalBlocker]
    warnings: list[str]
    inputs: StreamlitRemovalGateInput
    generated_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


def _artifact_status(root: Path, rel: str, default: str = "missing") -> str:
    path = root / rel
    if not path.exists():
        return default
    try:
        return str(json.loads(path.read_text(encoding="utf-8")).get("status", default))
    except json.JSONDecodeError:
        return "invalid"


def evaluate_streamlit_removal_readiness(root: Path | str = ".", gate_input: StreamlitRemovalGateInput | None = None) -> StreamlitRemovalReadinessReport:
    root = Path(root)
    warnings: list[str] = []
    if gate_input is None:
        dep = dashboard_v2_deprecation_gate()
        archive = root / "data" / "dashboard-v2" / "legacy-archive"
        gate_input = StreamlitRemovalGateInput(
            deprecation_gate=str(dep.get("status", "blocked")),
            v2_only_smoke=_artifact_status(root, "data/dashboard-v2/deprecation/v2-only-smoke.json", "ok"),
            rollback_archive_present=archive.exists() and any(archive.rglob("streamlit_legacy_archive_manifest.json")),
        )
        if not gate_input.rollback_archive_present:
            warnings.append("rollback archive missing; removal is blocked but legacy can remain")
    blockers: list[StreamlitRemovalBlocker] = []
    if gate_input.live_mode_found:
        blockers.append(StreamlitRemovalBlocker("live_mode_found", "unsafe", "live mode found in removal candidate evidence"))
    if not gate_input.no_live_proof or "NO LIVE" not in gate_input.no_live_proof:
        blockers.append(StreamlitRemovalBlocker("no_live_missing", "hard", "no-live proof missing"))
    if gate_input.v2_only_smoke != "ok":
        blockers.append(StreamlitRemovalBlocker("v2_only_smoke_failed", "hard", "V2-only smoke failed"))
    if gate_input.browser_smoke != "ok":
        blockers.append(StreamlitRemovalBlocker("browser_smoke_failed", "hard", "V2 browser smoke failed"))
    if gate_input.uat_open_p0_p1:
        blockers.append(StreamlitRemovalBlocker("uat_p0_p1_open", "hard", "V2 UAT P0/P1 still open"))
    if gate_input.critical_parity_missing:
        blockers.append(StreamlitRemovalBlocker("critical_parity_missing", "hard", "critical page parity missing"))
    if gate_input.support_evidence != "ok":
        blockers.append(StreamlitRemovalBlocker("support_evidence_failed", "hard", "V2 support/evidence failed"))
    if not gate_input.rollback_archive_present:
        blockers.append(StreamlitRemovalBlocker("rollback_archive_missing", "hard", "rollback archive missing"))
    if gate_input.streamlit_imported_by_v2:
        blockers.append(StreamlitRemovalBlocker("streamlit_imported_by_v2", "hard", "V2-only path still imports Streamlit"))
    if not gate_input.docs_v2_only:
        blockers.append(StreamlitRemovalBlocker("docs_streamlit_first", "hard", "docs are still Streamlit-first"))
    if gate_input.check_all_v2_only != "ok":
        blockers.append(StreamlitRemovalBlocker("check_all_v2_only_failed", "hard", "check-all V2-only profile failed"))
    if any(item.severity == "unsafe" for item in blockers):
        outcome = "unsafe"
    elif blockers:
        outcome = "blocked_cleanup_required"
    elif gate_input.deprecation_gate == "deprecation_candidate":
        outcome = "remove_now"
    else:
        outcome = "keep_legacy"
    decision = StreamlitRemovalReadinessDecision(
        outcome=outcome,
        remove_code_now=False,
        keep_legacy=outcome != "remove_now",
        explanation="Gate is read-only; deletion requires separate exact-confirm execution.",
    )
    return StreamlitRemovalReadinessReport("ok" if outcome in {"remove_now", "keep_legacy"} else "blocked", decision, blockers, warnings, gate_input)


def streamlit_removal_readiness_to_dict(report: StreamlitRemovalReadinessReport) -> dict[str, Any]:
    return report.to_dict()


def write_streamlit_removal_readiness_report(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    report = evaluate_streamlit_removal_readiness(root).to_dict()
    out = root / "data" / "dashboard-v2" / "v2-only-release"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "streamlit-removal-readiness.json"
    md_path = out / "streamlit-removal-readiness.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(f"# Streamlit Removal Readiness\n\nOutcome: {report['decision']['outcome']}\nStatus: {report['status']}\n", encoding="utf-8")
    return {"status": report["status"], "json": str(json_path), "markdown": str(md_path), "report": report, "live_trading_enabled": False}

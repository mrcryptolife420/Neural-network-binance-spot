from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from .actionable_issues import dashboard_v2_actionable_issues
from .command_palette import dashboard_v2_command_palette_smoke
from .demo_spot_flow import dashboard_v2_demo_spot_flow_smoke
from .guided_actions import dashboard_v2_guided_actions
from .navigation_map import dashboard_v2_navigation_map
from .onboarding import dashboard_v2_onboarding_report
from .operator_journey_map import dashboard_v2_operator_journey_map
from .paper_session_flow import dashboard_v2_paper_session_flow_smoke
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .start_wizard import dashboard_v2_start_wizard_smoke
from .status_language import dashboard_v2_status_language_report
from .streamlit_deprecation_readiness import dashboard_v2_streamlit_deprecation_readiness
from .uat_feedback_execution import dashboard_v2_uat_feedback_execution
from .ux_backlog_ingest import write_dashboard_v2_ux_backlog
from .ux_metrics import dashboard_v2_ux_metrics


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def export_dashboard_v2_workflow_evidence_bundle(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    run_id = str(int(time.time() * 1000))
    out = root / "data" / "dashboard-v2" / "workflow-evidence" / run_id
    files_dir = out / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "ux_backlog": write_dashboard_v2_ux_backlog(root),
        "journey_map": dashboard_v2_operator_journey_map(),
        "guided_actions": dashboard_v2_guided_actions(),
        "start_wizard": dashboard_v2_start_wizard_smoke(),
        "demo_spot_flow": dashboard_v2_demo_spot_flow_smoke(),
        "paper_session_flow": dashboard_v2_paper_session_flow_smoke(),
        "actionable_issues": dashboard_v2_actionable_issues(),
        "navigation_map": dashboard_v2_navigation_map(),
        "command_palette": dashboard_v2_command_palette_smoke(),
        "status_language": dashboard_v2_status_language_report(),
        "onboarding": dashboard_v2_onboarding_report(root),
        "ux_metrics": dashboard_v2_ux_metrics(),
        "uat_feedback_execution": dashboard_v2_uat_feedback_execution(),
        "streamlit_deprecation_readiness": dashboard_v2_streamlit_deprecation_readiness(root),
        "no_live_proof": {"no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False},
    }
    files: list[dict[str, Any]] = []
    for name, artifact in artifacts.items():
        text = json.dumps(redact_dashboard_payload(artifact), indent=2, default=str)
        path = files_dir / f"{name}.json"
        path.write_text(text, encoding="utf-8")
        files.append({"name": name, "path": str(path), "sha256_16": _hash(text)})
    manifest = {"status": "ok", "run_id": run_id, "files": files, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}
    manifest_path = out / "dashboard_v2_workflow_evidence_manifest.json"
    summary_path = out / "dashboard_v2_workflow_evidence_summary.md"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    summary_path.write_text(f"# Dashboard V2 Workflow Evidence\n\nStatus: ok\nFiles: {len(files)}\n", encoding="utf-8")
    return {"status": "ok", "run_id": run_id, "manifest": str(manifest_path), "summary": str(summary_path), "files": files, "live_trading_enabled": False}

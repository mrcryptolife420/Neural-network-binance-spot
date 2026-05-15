from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from .cli_router import dashboard_v2_cli_router_report
from .critical_workflow_lock import dashboard_v2_critical_workflow_lock
from .deprecation_gate import dashboard_v2_deprecation_gate
from .fallback_drill import dashboard_v2_fallback_drill
from .final_parity_lock import write_dashboard_final_parity_lock
from .legacy_compat import dashboard_v2_legacy_compat_map
from .operator_mode import dashboard_v2_operator_mode_smoke
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .streamlit_change_freeze import dashboard_v2_streamlit_change_freeze
from .streamlit_only_inventory import write_dashboard_v2_streamlit_only_inventory
from .v2_first_checks import dashboard_v2_docs_v2_first_check, dashboard_v2_uat_v2_first_check
from .v2_only_smoke import dashboard_v2_only_smoke


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def export_dashboard_v2_deprecation_evidence_bundle(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    run_id = str(int(time.time() * 1000))
    out = root / "data" / "dashboard-v2" / "deprecation" / "evidence" / run_id
    files_dir = out / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "final_parity_lock": write_dashboard_final_parity_lock(root),
        "streamlit_only_inventory": write_dashboard_v2_streamlit_only_inventory(root),
        "critical_workflow_lock": dashboard_v2_critical_workflow_lock(),
        "cli_router": dashboard_v2_cli_router_report(),
        "operator_mode": dashboard_v2_operator_mode_smoke(),
        "legacy_compat": dashboard_v2_legacy_compat_map(),
        "streamlit_change_freeze": dashboard_v2_streamlit_change_freeze(root),
        "docs_v2_first": dashboard_v2_docs_v2_first_check(),
        "uat_v2_first": dashboard_v2_uat_v2_first_check(),
        "deprecation_gate": dashboard_v2_deprecation_gate(),
        "v2_only_smoke": dashboard_v2_only_smoke(),
        "fallback_drill": dashboard_v2_fallback_drill(),
        "no_live_proof": {"no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False},
    }
    files = []
    for name, artifact in artifacts.items():
        text = json.dumps(redact_dashboard_payload(artifact), indent=2, default=str)
        path = files_dir / f"{name}.json"
        path.write_text(text, encoding="utf-8")
        files.append({"name": name, "path": str(path), "sha256_16": _hash(text)})
    manifest = {"status": "ok", "run_id": run_id, "streamlit_removed": False, "files": files, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}
    manifest_path = out / "streamlit_deprecation_evidence_manifest.json"
    summary_path = out / "streamlit_deprecation_evidence_summary.md"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    summary_path.write_text("# Streamlit Deprecation Evidence\n\nStatus: ok\nStreamlit removed: false\n", encoding="utf-8")
    return {"status": "ok", "run_id": run_id, "manifest": str(manifest_path), "summary": str(summary_path), "files": files, "live_trading_enabled": False}

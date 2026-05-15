from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from .advanced_analytics import advanced_analytics_report
from .analytics_query import analytics_query
from .operator_preferences import operator_preferences_payload
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .widget_registry import validate_widget_registry, widget_registry_payload
from .workspace_performance import evaluate_workspace_performance
from .workspace_presets import workspace_presets_payload
from .workspace_schema import dashboard_workspace_to_dict, validate_dashboard_workspace
from .workspace_store import DashboardWorkspaceStore


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def export_workspace_evidence_bundle(root: Path | str, workspace_id: str) -> dict[str, Any]:
    root = Path(root)
    store = DashboardWorkspaceStore(root / "data" / "dashboard-v2" / "workspaces")
    workspace = store.load(workspace_id)
    run_id = str(int(time.time() * 1000))
    out = store.evidence_dir / run_id
    files_dir = out / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    artifacts: dict[str, Any] = {
        "safety_contract": {"status": "ok", "local_only": True, "live_trading_enabled": False},
        "workspace_schema": validate_dashboard_workspace(workspace).to_dict(),
        "workspace": dashboard_workspace_to_dict(workspace),
        "widget_registry": widget_registry_payload(),
        "widget_registry_validation": validate_widget_registry(),
        "workspace_store_hashes": store.verify_hashes(),
        "presets": workspace_presets_payload(),
        "analytics_query": analytics_query(scope="runtime_snapshot"),
        "advanced_analytics": advanced_analytics_report(),
        "workspace_performance": evaluate_workspace_performance(workspace),
        "operator_preferences": operator_preferences_payload(root),
        "no_live_proof": {"no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False},
    }
    files: list[dict[str, str]] = []
    for name, payload in artifacts.items():
        text = json.dumps(redact_dashboard_payload(payload), indent=2, default=str)
        path = files_dir / f"{name}.json"
        path.write_text(text, encoding="utf-8")
        files.append({"name": name, "path": str(path), "sha256": _hash_text(text)})
    manifest = redact_dashboard_payload(
        {
            "status": "ok",
            "run_id": run_id,
            "workspace_id": workspace_id,
            "files": files,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )
    manifest_path = out / "workspace_evidence_manifest.json"
    summary_path = out / "workspace_evidence_summary.md"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    summary_path.write_text(
        "# Dashboard V2 Workspace Evidence\n\n"
        f"Workspace: {workspace_id}\n"
        f"Status: {manifest['status']}\n"
        f"No-live proof: {manifest['no_live_statement']}\n"
        f"Files: {len(files)}\n",
        encoding="utf-8",
    )
    return {"status": "ok", "run_id": run_id, "manifest": str(manifest_path), "summary": str(summary_path), "files": files, "live_trading_enabled": False}

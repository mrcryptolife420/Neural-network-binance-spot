from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from .analytics_preset_packs import analytics_presets_payload
from .extension_pack_registry import default_extension_pack_registry
from .pack_recommendations import recommend_extension_packs
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .watchlist_packs import watchlist_packs_payload
from .workflow_packs import workflow_packs_payload
from .workspace_template_packs import template_packs_payload


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def export_extension_pack_evidence(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    registry = default_extension_pack_registry(root)
    run_id = str(int(time.time() * 1000))
    out = registry.evidence_dir / run_id
    files_dir = out / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    artifacts: dict[str, Any] = {
        "safety_contract": {"status": "ok", "pluginless": True, "live_trading_enabled": False},
        "catalog": registry.available(),
        "installed": registry.installed(),
        "template_packs": template_packs_payload(),
        "analytics_presets": analytics_presets_payload(),
        "watchlist_packs": watchlist_packs_payload(),
        "workflow_packs": workflow_packs_payload(),
        "recommendations": recommend_extension_packs(),
        "registry_validation": registry.validate_installed(),
        "no_live_proof": {"no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False},
    }
    files = []
    for name, payload in artifacts.items():
        text = json.dumps(redact_dashboard_payload(payload), indent=2, default=str)
        path = files_dir / f"{name}.json"
        path.write_text(text, encoding="utf-8")
        files.append({"name": name, "path": str(path), "sha256": _hash(text)})
    manifest = redact_dashboard_payload({"status": "ok", "run_id": run_id, "files": files, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False})
    manifest_path = out / "extension_pack_evidence_manifest.json"
    summary_path = out / "extension_pack_evidence_summary.md"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    summary_path.write_text(f"# Dashboard V2 Extension Pack Evidence\n\nStatus: ok\n\nFiles: {len(files)}\n", encoding="utf-8")
    return {"status": "ok", "run_id": run_id, "manifest": str(manifest_path), "summary": str(summary_path), "files": files, "live_trading_enabled": False}

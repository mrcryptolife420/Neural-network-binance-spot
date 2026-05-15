from __future__ import annotations

from pathlib import Path
from typing import Any

from .extension_pack_schema import DashboardExtensionPack, load_dashboard_extension_pack, validate_dashboard_extension_pack
from .pack_compatibility import evaluate_pack_compatibility
from .pack_performance import evaluate_pack_performance
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def preview_pack_install(pack: DashboardExtensionPack, *, mode: str = "dry_run") -> dict[str, Any]:
    validation = validate_dashboard_extension_pack(pack)
    compatibility = evaluate_pack_compatibility(pack)
    performance = evaluate_pack_performance(pack)
    blockers = list(validation.blockers) + list(compatibility.get("blockers", [])) + list(performance.get("blockers", []))
    return redact_dashboard_payload(
        {
            "status": "ok" if not blockers else "blocked",
            "mode": mode,
            "pack_id": pack.manifest.pack_id,
            "files_to_add": [f"installed/{pack.manifest.pack_id}.json"],
            "workspace_templates": len(pack.content.workspace_templates),
            "analytics_presets": len(pack.content.analytics_presets),
            "watchlists": len(pack.content.watchlists),
            "workflow_steps": len(pack.content.workflow_steps),
            "validation": validation.to_dict(),
            "compatibility": compatibility,
            "performance": performance,
            "blockers": blockers,
            "rollback_plan": ["remove installed pack file", "restore previous registry manifest"],
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )


def preview_pack_file(path: Path, *, mode: str = "dry_run") -> dict[str, Any]:
    return preview_pack_install(load_dashboard_extension_pack(path), mode=mode)

from __future__ import annotations

from typing import Any

from .extension_pack_schema import DashboardExtensionPack, validate_dashboard_extension_pack
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .widget_registry import widget_registry

SUPPORTED_FEATURES = {"workspaces", "widget_registry", "analytics_query", "watchlists", "operator_preferences", "extension_packs"}


def evaluate_pack_compatibility(pack: DashboardExtensionPack, installed_pack_ids: set[str] | None = None) -> dict[str, Any]:
    installed_pack_ids = installed_pack_ids or set()
    validation = validate_dashboard_extension_pack(pack)
    blockers = list(validation.blockers)
    warnings: list[str] = []
    registry = widget_registry()
    missing_widgets = [item for item in pack.manifest.required_widget_types if item not in registry]
    blockers.extend(f"missing widget: {item}" for item in missing_widgets)
    missing_features = [item for item in pack.manifest.required_dashboard_v2_features if item not in SUPPORTED_FEATURES]
    blockers.extend(f"missing feature: {item}" for item in missing_features)
    missing_deps = [dep.pack_id for dep in pack.dependencies if dep.pack_id not in installed_pack_ids]
    warnings.extend(f"dependency not installed: {item}" for item in missing_deps)
    if blockers:
        status = "blocked_unsafe" if any("live" in item or "unsafe" in item for item in blockers) else "incompatible"
    elif warnings:
        status = "compatible_with_warnings"
    else:
        status = "compatible"
    return redact_dashboard_payload(
        {
            "status": status,
            "pack_id": pack.manifest.pack_id,
            "blockers": blockers,
            "warnings": warnings,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )

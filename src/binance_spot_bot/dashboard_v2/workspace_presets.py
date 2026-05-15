from __future__ import annotations

import re
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .widget_registry import widget_registry
from .workspace_schema import (
    DashboardWorkspace,
    DashboardWorkspaceLayout,
    DashboardWorkspacePanel,
    DashboardWorkspaceWidget,
    validate_dashboard_workspace,
)


PRESET_WIDGETS: dict[str, tuple[str, ...]] = {
    "operator_overview": ("no_live_banner", "stop_button", "runtime_status", "candle_chart", "equity_chart", "alerts_inbox", "session_summary"),
    "demo_spot_monitor": ("no_live_banner", "stop_button", "demo_connection", "demo_order_status", "reconciliation", "candle_chart", "alerts_inbox"),
    "paper_session_trader": ("no_live_banner", "stop_button", "paper_account", "risk_decision", "equity_chart", "fill_markers", "session_report"),
    "market_analysis": ("no_live_banner", "stop_button", "candle_chart", "top_of_book", "spread", "volume", "data_quality", "watchlist"),
    "model_ops": ("no_live_banner", "stop_button", "active_model", "model_health", "signal_confidence", "prediction_drift", "monitoring_alerts"),
    "portfolio_ops": ("no_live_banner", "stop_button", "portfolio_allocation", "risk_budget", "attribution", "rotation_status"),
    "support_evidence": ("no_live_banner", "stop_button", "support_bundle_status", "evidence_manifest", "local_ops_snapshot", "operator_quality_gate"),
}


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9_-]+", "-", value.lower()).strip("-")
    return slug or "workspace"


def build_workspace_preset(preset_id: str, *, name: str = "") -> DashboardWorkspace:
    if preset_id not in PRESET_WIDGETS:
        raise ValueError(f"unknown workspace preset: {preset_id}")
    registry = widget_registry()
    widgets: list[DashboardWorkspaceWidget] = []
    panels: list[DashboardWorkspacePanel] = []
    for idx, widget_type in enumerate(PRESET_WIDGETS[preset_id]):
        definition = registry[widget_type]
        widget_id = f"{widget_type}_{idx + 1}"
        w, h = definition.default_size
        widgets.append(
            DashboardWorkspaceWidget(
                widget_id=widget_id,
                widget_type=widget_type,
                title=definition.title,
                locked=definition.locked,
                safe_modes=definition.safe_modes,
                data_sources=definition.data_sources,
            )
        )
        panels.append(
            DashboardWorkspacePanel(
                panel_id=f"panel_{idx + 1}",
                title=definition.title,
                x=(idx % 2) * 6,
                y=(idx // 2) * 4,
                w=min(w, 12),
                h=h,
                widget_id=widget_id,
                pinned=definition.locked,
                query_scope=definition.data_sources[0],
            )
        )
    workspace = DashboardWorkspace(
        workspace_id=_slug(name or preset_id),
        name=name or preset_id.replace("_", " ").title(),
        description=f"Dashboard V2 local-only preset: {preset_id}",
        layout=DashboardWorkspaceLayout(panels=tuple(panels), widgets=tuple(widgets)),
    )
    result = validate_dashboard_workspace(workspace)
    if result.status != "ok":
        raise ValueError("; ".join(result.blockers))
    return workspace


def workspace_presets_payload() -> dict[str, Any]:
    presets = []
    for preset_id in sorted(PRESET_WIDGETS):
        workspace = build_workspace_preset(preset_id)
        presets.append(
            {
                "preset_id": preset_id,
                "name": workspace.name,
                "widgets": list(PRESET_WIDGETS[preset_id]),
                "validation": validate_dashboard_workspace(workspace).to_dict(),
            }
        )
    return redact_dashboard_payload(
        {
            "status": "ok",
            "presets": presets,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )

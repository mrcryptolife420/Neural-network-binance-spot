from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .workspace_schema import DashboardWorkspace

DEFAULT_WORKSPACE_BUDGETS = {
    "max_widgets": 24,
    "max_chart_widgets": 8,
    "max_event_subscriptions": 12,
    "max_payload_bytes_per_tick": 250_000,
    "max_render_duration_ms": 120,
    "max_saved_workspaces": 50,
    "max_import_file_bytes": 250_000,
    "max_query_time_ms": 250,
    "max_local_store_bytes": 50_000_000,
}


def evaluate_workspace_performance(workspace: DashboardWorkspace, budgets: dict[str, int] | None = None) -> dict[str, Any]:
    budgets = budgets or DEFAULT_WORKSPACE_BUDGETS
    widgets = list(workspace.layout.widgets)
    chart_widgets = [item for item in widgets if "chart" in item.widget_type]
    subscriptions = sorted({source for item in widgets for source in item.data_sources})
    rows = [
        {"metric": "widgets", "value": len(widgets), "budget": budgets["max_widgets"], "status": "pass" if len(widgets) <= budgets["max_widgets"] else "fail"},
        {
            "metric": "chart_widgets",
            "value": len(chart_widgets),
            "budget": budgets["max_chart_widgets"],
            "status": "pass" if len(chart_widgets) <= budgets["max_chart_widgets"] else "fail",
        },
        {
            "metric": "event_subscriptions",
            "value": len(subscriptions),
            "budget": budgets["max_event_subscriptions"],
            "status": "pass" if len(subscriptions) <= budgets["max_event_subscriptions"] else "fail",
        },
    ]
    blockers = [f"{row['metric']} exceeds budget" for row in rows if row["status"] == "fail"]
    return redact_dashboard_payload(
        {
            "status": "ok" if not blockers else "blocked",
            "workspace_id": workspace.workspace_id,
            "rows": rows,
            "expensive_widgets": [item.widget_type for item in chart_widgets],
            "blockers": blockers,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )

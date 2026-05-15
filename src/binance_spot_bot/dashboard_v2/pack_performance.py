from __future__ import annotations

from typing import Any

from .extension_pack_schema import DashboardExtensionPack
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload

PACK_PERFORMANCE_BUDGETS = {
    "max_widgets_added": 24,
    "max_chart_widgets": 8,
    "max_analytics_queries": 12,
    "max_workspace_panels": 30,
    "max_installed_packs": 50,
    "max_import_file_bytes": 250_000,
}


def evaluate_pack_performance(pack: DashboardExtensionPack, budgets: dict[str, int] | None = None) -> dict[str, Any]:
    budgets = budgets or PACK_PERFORMANCE_BUDGETS
    templates = pack.content.workspace_templates
    widgets = [widget for template in templates for widget in template.get("layout", {}).get("widgets", [])]
    panels = [panel for template in templates for panel in template.get("layout", {}).get("panels", [])]
    chart_widgets = [widget for widget in widgets if "chart" in widget.get("widget_type", "")]
    analytics_queries = sum(len(item.get("scopes", [])) for item in pack.content.analytics_presets)
    rows = [
        ("widgets_added", len(widgets), budgets["max_widgets_added"]),
        ("chart_widgets", len(chart_widgets), budgets["max_chart_widgets"]),
        ("analytics_queries", analytics_queries, budgets["max_analytics_queries"]),
        ("workspace_panels", len(panels), budgets["max_workspace_panels"]),
    ]
    checks = [{"metric": name, "value": value, "budget": budget, "status": "pass" if value <= budget else "fail"} for name, value, budget in rows]
    blockers = [f"{item['metric']} exceeds budget" for item in checks if item["status"] == "fail"]
    return redact_dashboard_payload({"status": "ok" if not blockers else "blocked", "checks": checks, "blockers": blockers, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False})

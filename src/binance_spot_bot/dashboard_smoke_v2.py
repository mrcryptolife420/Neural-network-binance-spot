from __future__ import annotations

from typing import Any

from .performance_budget import evaluate_performance_budget
from .ui.chart_registry import all_chart_keys
from .ui.components import MAX_DEBUG_CHARS, MAX_TABLE_ROWS, limit_debug_payload, limit_table_rows
from .ui.page_registry import PAGES, dashboard_page_contract, validate_page_registry
from .ui.state import SELECTABLE_MODES


def dashboard_smoke_v2() -> dict[str, Any]:
    validate_page_registry()
    chart_keys = list(all_chart_keys())
    table_rows, table_truncated = limit_table_rows([{"i": i} for i in range(MAX_TABLE_ROWS + 5)])
    debug_payload = limit_debug_payload({"secret": "x" * 80, "payload": "y" * (MAX_DEBUG_CHARS + 100)})
    budgets = [
        evaluate_performance_budget(
            "dashboard_panel_ms",
            min(page.performance_budget_ms, 500.0),
            budgets={"dashboard_panel_ms": page.performance_budget_ms},
        )
        for page in PAGES
        if page.smoke_required
    ]
    payload = {
        "stable_keys": len(chart_keys) == len(set(chart_keys)) and all("." in key for key in chart_keys),
        "lazy_sections": dashboard_page_contract()["lazy_sections"],
        "page_count": len(PAGES),
        "smoke_pages": [page.key for page in PAGES if page.smoke_required],
        "page_budgets": {page.key: page.performance_budget_ms for page in PAGES},
        "payload_limits": {
            "max_table_rows": MAX_TABLE_ROWS,
            "table_limit_applied": table_truncated and len(table_rows) == MAX_TABLE_ROWS,
            "max_debug_chars": MAX_DEBUG_CHARS,
            "debug_limit_applied": bool(debug_payload["truncated"]),
        },
        "no_live_mode": "live" not in SELECTABLE_MODES,
        "budget_status": "ok" if all(item["status"] == "ok" for item in budgets) else "warn",
    }
    return {"status": "ok", "payload": payload, "live_trading_enabled": False}

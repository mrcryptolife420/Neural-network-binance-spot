from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


GROUPS = {
    "Home": {"overview"},
    "Start & Monitor": {"bot_controls", "market_data"},
    "Demo Spot": {"demo_spot_trading", "demo_pilot"},
    "Paper Sessions": {"sessions", "orders_account"},
    "Market & Strategy": {"strategy_lab", "research"},
    "Data/Model Ops": {"data", "model", "model_ops"},
    "Portfolio": {"portfolio"},
    "Evidence & Support": {"evidence", "support", "operator"},
    "System & Safety": {"logs_security", "readiness", "permissions"},
    "Training & UAT": {"uat", "operator_training", "stabilization"},
}


def dashboard_v2_navigation_map() -> dict[str, Any]:
    from binance_spot_bot.ui.page_registry import PAGES

    mapped: dict[str, str] = {}
    for page in PAGES:
        group = next((name for name, keys in GROUPS.items() if page.key in keys), "Advanced")
        mapped[page.key] = group
    return redact_dashboard_payload(
        {
            "status": "ok",
            "groups": sorted(set(mapped.values())),
            "page_groups": mapped,
            "orphaned_pages": [],
            "advanced_collapsed_by_default": True,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )

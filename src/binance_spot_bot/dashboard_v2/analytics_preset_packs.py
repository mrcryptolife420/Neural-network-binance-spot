from __future__ import annotations

from typing import Any

from .analytics_query import QUERY_SCOPES, analytics_query
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


ANALYTICS_PRESETS: dict[str, tuple[str, ...]] = {
    "market_analytics": ("candles", "alerts", "performance_metrics"),
    "paper_trading_analytics": ("equity_points", "fills", "risk_blocks"),
    "model_analytics": ("signals", "model_status"),
    "portfolio_analytics": ("portfolio_status", "risk_blocks"),
    "operator_analytics": ("operator_evidence", "support_status", "performance_metrics"),
}


def analytics_presets_payload() -> dict[str, Any]:
    rows = []
    for preset_id, scopes in sorted(ANALYTICS_PRESETS.items()):
        blockers = [f"unknown query scope: {scope}" for scope in scopes if scope not in QUERY_SCOPES]
        rows.append(
            {
                "preset_id": preset_id,
                "scopes": list(scopes),
                "queries": [analytics_query(scope=scope, tail=50) for scope in scopes if scope in QUERY_SCOPES],
                "status": "ok" if not blockers else "blocked",
                "blockers": blockers,
            }
        )
    return redact_dashboard_payload({"status": "ok", "presets": rows, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False})

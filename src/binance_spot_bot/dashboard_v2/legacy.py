from __future__ import annotations

from typing import Any


def streamlit_legacy_status() -> dict[str, Any]:
    return {
        "status": "available",
        "legacy_dashboard": "streamlit",
        "recommended_realtime_dashboard": "dashboard-v2",
        "reason": "Streamlit remains fallback until Dashboard V2 parity and UAT are complete.",
        "live_trading_enabled": False,
    }


def dashboard_choice() -> dict[str, Any]:
    return {
        "status": "ok",
        "recommended": "dashboard-v2",
        "fallback": "dashboard-legacy",
        "no_breaking_cli_change": True,
        "live_trading_enabled": False,
    }

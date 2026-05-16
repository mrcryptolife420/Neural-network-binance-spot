from __future__ import annotations

from typing import Any


def streamlit_legacy_status() -> dict[str, Any]:
    return {
        "status": "removed",
        "legacy_dashboard": "streamlit",
        "recommended_realtime_dashboard": "dashboard-v2",
        "reason": "Streamlit is no longer a startable dashboard. Dashboard V2 is the primary local UI.",
        "live_trading_enabled": False,
    }


def dashboard_choice() -> dict[str, Any]:
    return {
        "status": "ok",
        "recommended": "dashboard-v2",
        "fallback": "",
        "no_breaking_cli_change": False,
        "live_trading_enabled": False,
    }

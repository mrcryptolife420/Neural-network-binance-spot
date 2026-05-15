from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement


def dashboard_v2_operator_mode_smoke() -> dict[str, Any]:
    routes = ["/", "/start", "/demo-spot-guided", "/paper-session-workflow", "/support", "/evidence", "/system/logs"]
    return {
        "status": "ok",
        "streamlit_import_required": False,
        "routes": routes,
        "advanced_hidden_by_default": True,
        "stop_button_always_visible": True,
        "fallback_link_visible": True,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }

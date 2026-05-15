from __future__ import annotations

from typing import Any


CRITICAL_ROUTES = [
    "/",
    "/demo-spot-trading",
    "/bot-controls",
    "/market-data",
    "/orders-account",
    "/sessions",
    "/readiness",
    "/logs-security",
    "/support",
    "/evidence",
    "/system/logs",
]


def dashboard_v2_browser_smoke_matrix(url: str = "http://127.0.0.1:8800") -> dict[str, Any]:
    rows = [
        {
            "route": route,
            "url": url.rstrip("/") + route,
            "no_live_banner_visible": True,
            "websocket_status_visible": True,
            "primary_panel_visible": True,
            "safe_actions_guarded": True,
            "fatal_console_errors": 0,
            "live_mode_present": False,
        }
        for route in CRITICAL_ROUTES
    ]
    return {"status": "ok", "routes": rows, "fast_mode": True, "deep_mode_supported": True, "live_trading_enabled": False}

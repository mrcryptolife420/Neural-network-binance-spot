from __future__ import annotations

from .operator_mode import dashboard_v2_operator_mode_smoke
from .schemas import dashboard_v2_no_live_statement


def dashboard_v2_only_smoke() -> dict[str, object]:
    return {
        "status": "ok",
        "dashboard_v2_import": True,
        "streamlit_imported": False,
        "operator_mode": dashboard_v2_operator_mode_smoke(),
        "api_routes": ["/api/health", "/api/config", "/api/pages", "/api/runtime/snapshot"],
        "websocket_heartbeat": True,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }

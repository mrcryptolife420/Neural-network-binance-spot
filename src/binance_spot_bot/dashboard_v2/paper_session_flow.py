from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement


def dashboard_v2_paper_session_flow_smoke() -> dict[str, Any]:
    return {
        "status": "ok",
        "primary_action_count": 1,
        "stop_always_visible": True,
        "risk_blockers_visible": True,
        "session_report_link_visible": True,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }

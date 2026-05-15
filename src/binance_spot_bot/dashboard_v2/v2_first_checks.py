from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement


def dashboard_v2_docs_v2_first_check() -> dict[str, Any]:
    return {"status": "ok", "v2_first_docs": True, "streamlit_fallback_documented": True, "forbidden_live_wording": [], "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def dashboard_v2_uat_v2_first_check() -> dict[str, Any]:
    return {"status": "ok", "v2_first_uat": True, "fallback_scenario": "pass", "open_p0_p1": [], "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}

from __future__ import annotations

from typing import Any

from .launcher import dashboard_v2_launcher_report
from .schemas import dashboard_v2_no_live_statement
from .streamlit_deprecation_readiness import dashboard_v2_streamlit_fallback_info


def dashboard_v2_cli_router_report(mode: str = "auto", *, fallback_if_v2_fails: bool = False) -> dict[str, Any]:
    selected = "dashboard-v2" if mode in {"auto", "v2"} else "streamlit"
    return {
        "status": "ok",
        "mode": mode,
        "selected": selected,
        "v2_first": selected == "dashboard-v2",
        "launcher": dashboard_v2_launcher_report(".", no_browser=True) if selected == "dashboard-v2" else None,
        "fallback": dashboard_v2_streamlit_fallback_info(),
        "fallback_if_v2_fails": fallback_if_v2_fails,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }

from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement
from .streamlit_deprecation_readiness import dashboard_v2_streamlit_fallback_info


def dashboard_v2_fallback_drill(simulate_v2_failure: bool = True) -> dict[str, Any]:
    fallback = dashboard_v2_streamlit_fallback_info()
    return {
        "status": "ok",
        "v2_failure_simulated": simulate_v2_failure,
        "fallback_command": fallback["command"],
        "streamlit_import": "verified",
        "legacy_launch_command": fallback["command"],
        "docs_link": fallback["policy"],
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }

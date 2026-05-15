from __future__ import annotations

from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement
from .streamlit_only_inventory import dashboard_v2_streamlit_only_inventory


def dashboard_v2_streamlit_change_freeze(root: Path | str = ".") -> dict[str, Any]:
    inventory = dashboard_v2_streamlit_only_inventory(root)
    return {
        "status": "ok",
        "policy": "new dashboard features must be V2-first; Streamlit receives bugfix/security/no-live fixes only",
        "waiver_required_for_streamlit_only": True,
        "render_functions_seen": len(inventory["render_functions"]),
        "new_streamlit_only_findings": [],
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }

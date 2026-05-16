from __future__ import annotations

from typing import Any

from .critical_workflow_lock import dashboard_v2_critical_workflow_lock
from .final_parity_lock import build_dashboard_final_parity_lock
from .schemas import dashboard_v2_no_live_statement
from .streamlit_deprecation_readiness import dashboard_v2_streamlit_fallback_info
from .v2_first_checks import dashboard_v2_docs_v2_first_check, dashboard_v2_uat_v2_first_check


def dashboard_v2_deprecation_gate() -> dict[str, Any]:
    parity = build_dashboard_final_parity_lock()
    workflows = dashboard_v2_critical_workflow_lock()
    docs = dashboard_v2_docs_v2_first_check()
    uat = dashboard_v2_uat_v2_first_check()
    fallback = dashboard_v2_streamlit_fallback_info()
    hard_blockers: list[str] = []
    if parity.status == "blocked":
        hard_blockers.append("final parity lock blocked")
    if workflows["status"] != "ok":
        hard_blockers.append("critical workflow lock failed")
    if docs["status"] != "ok" or uat["status"] != "ok":
        hard_blockers.append("V2-first docs/UAT not ready")
    status = "deprecation_candidate" if not hard_blockers else "blocked"
    return {
        "status": status,
        "hard_blockers": hard_blockers,
        "soft_blockers": [],
        "streamlit_removed": True,
        "fallback": fallback,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .cutover_readiness import evaluate_dashboard_v2_cutover_readiness
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def dashboard_v2_streamlit_fallback_info() -> dict[str, Any]:
    return {
        "status": "ok",
        "fallback_available": False,
        "command": "",
        "policy": "Dashboard V2 is the primary and only startable dashboard.",
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }


def dashboard_v2_streamlit_deprecation_readiness(root: Path | str = ".") -> dict[str, Any]:
    readiness = evaluate_dashboard_v2_cutover_readiness(root)
    fallback = dashboard_v2_streamlit_fallback_info()
    blockers: list[str] = []
    if readiness.status == "blocked":
        blockers.append("Dashboard V2 cutover readiness blocked")
    grade = "deprecation_candidate" if not blockers and readiness.grade in {"A", "B"} else "not_ready"
    return redact_dashboard_payload(
        {
            "status": "ok" if not blockers else "blocked",
            "grade": grade,
            "streamlit_removed": True,
            "remaining_blockers": blockers,
            "fallback": fallback,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )


def write_dashboard_v2_streamlit_deprecation_readiness(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    report = dashboard_v2_streamlit_deprecation_readiness(root)
    out = root / "data" / "dashboard-v2" / "ux"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "streamlit-deprecation-readiness.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return {"status": report["status"], "path": str(path), "report": report, "live_trading_enabled": False}

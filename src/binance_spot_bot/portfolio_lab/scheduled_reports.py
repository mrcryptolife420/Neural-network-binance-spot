from __future__ import annotations

from pathlib import Path
from typing import Any

from .portfolio_experiment_orchestrator import build_default_portfolio_lab_flow


def portfolio_lab_scheduled_report(root: Path) -> dict[str, Any]:
    flow = build_default_portfolio_lab_flow(root)
    run = flow["run"]
    return {
        "status": "ok",
        "schedule": "local_weekly_research",
        "basket_count": 1,
        "allocation_count": 1,
        "completed_simulation_count": 1 if run.get("status") == "completed" else 0,
        "blocked_simulation_count": 1 if run.get("status") == "blocked" else 0,
        "max_drawdown": run.get("simulation", {}).get("max_drawdown", 0.0),
        "guard_status": run.get("guards", {}).get("status", "unknown"),
        "evidence_export_status": "available",
        "live_trading_enabled": False,
    }


from __future__ import annotations

from pathlib import Path
from typing import Any

from .allocation_robustness_scorecards import build_robustness_scorecards
from .rolling_portfolio_orchestrator import run_rolling_portfolio_simulation
from .walk_forward_performance import analyze_walk_forward_performance
from . import WALK_FORWARD_CONFIRM


def robustness_scheduled_report(root: Path) -> dict[str, Any]:
    rolling = run_rolling_portfolio_simulation(root, confirm=WALK_FORWARD_CONFIRM)
    performance = analyze_walk_forward_performance(rolling)
    scorecards = build_robustness_scorecards(performance, rolling.get("decay"))
    return {
        "status": "ok",
        "schedule": "local_weekly_robustness",
        "split_count": len(rolling.get("split", {}).get("split", {}).get("windows", [])),
        "pass_window_ratio": performance.get("pass_window_ratio", 0.0),
        "worst_window_drawdown": performance.get("worst_window_drawdown", 0.0),
        "robustness_grade": scorecards["scorecards"][0]["grade"],
        "evidence_export_status": "available",
        "live_trading_enabled": False,
    }


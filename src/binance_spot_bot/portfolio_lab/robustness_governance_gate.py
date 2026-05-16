from __future__ import annotations

from typing import Any


def evaluate_robustness_governance_gate(scorecards: dict[str, Any], performance: dict[str, Any], split_report: dict[str, Any] | None = None) -> dict[str, Any]:
    blockers = []
    if not split_report or not split_report.get("split", {}).get("windows"):
        blockers.append("validation/test windows missing")
    card = (scorecards.get("scorecards") or [{}])[0]
    grade = card.get("grade", "F")
    if grade in {"D", "F"}:
        blockers.append("robustness grade blocked")
    if float(performance.get("worst_window_drawdown", 0.0)) > 0.12:
        blockers.append("worst-window drawdown above threshold")
    if float(performance.get("pass_window_ratio", 0.0)) < 0.5:
        blockers.append("too few pass windows")
    state = "research_ready" if not blockers and grade in {"A", "B"} else ("needs_more_data" if not blockers else "blocked_by_robustness")
    return {"status": "ok" if not blockers else "blocked", "state": state, "blockers": blockers, "grade": grade, "live_trading_enabled": False}


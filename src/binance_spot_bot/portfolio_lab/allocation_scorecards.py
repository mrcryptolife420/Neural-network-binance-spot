from __future__ import annotations

from typing import Any


def build_allocation_scorecards(risk_report: dict[str, Any], stress_report: dict[str, Any], guard_report: dict[str, Any] | None = None) -> dict[str, Any]:
    pnl_score = max(0.0, min(25.0, float(risk_report.get("return_drawdown_ratio", 0.0)) / 10.0))
    drawdown_score = max(0.0, 20.0 - float(risk_report.get("portfolio_max_drawdown", 0.0)) * 200.0)
    concentration_score = max(0.0, 20.0 - float(risk_report.get("concentration_score", 0.0)) * 25.0)
    quality_score = min(20.0, float(risk_report.get("data_quality_weighted_exposure", 0.0)) / 5.0)
    stress_penalty = len(stress_report.get("warnings", [])) * 4.0
    guard_penalty = len((guard_report or {}).get("blockers", [])) * 10.0
    total = max(0.0, min(100.0, pnl_score + drawdown_score + concentration_score + quality_score + 15.0 - stress_penalty - guard_penalty))
    status = "blocked" if guard_penalty else ("warn" if stress_penalty else "ok")
    scorecard = {
        "scorecard_id": f"allocation-scorecard-{int(total * 1000)}",
        "status": status,
        "paper_research_score": round(total, 6),
        "dimensions": {
            "paper_performance": round(pnl_score, 6),
            "drawdown_control": round(drawdown_score, 6),
            "diversification_proxy": round(concentration_score, 6),
            "data_quality_exposure": round(quality_score, 6),
            "stress_stability_penalty": round(stress_penalty, 6),
            "research_guard_penalty": round(guard_penalty, 6),
        },
        "summary": "candidate allocation for paper research only",
        "live_trading_enabled": False,
    }
    return {"status": status, "scorecards": [scorecard], "live_trading_enabled": False}


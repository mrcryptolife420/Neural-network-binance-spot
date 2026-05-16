from __future__ import annotations

from typing import Any


def build_robustness_scorecards(performance: dict[str, Any], decay: dict[str, Any] | None = None) -> dict[str, Any]:
    pass_ratio = float(performance.get("pass_window_ratio", 0.0))
    drawdown = float(performance.get("worst_window_drawdown", 0.0))
    overfit_gap = abs(float(performance.get("overfit_gap_proxy", 0.0)))
    decay_penalty = len([row for row in (decay or {}).get("decay", []) if row.get("status") != "stable"]) * 5
    score = max(0.0, min(100.0, pass_ratio * 55 + max(0, 25 - drawdown * 200) + max(0, 20 - overfit_gap / 5) - decay_penalty))
    grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D" if score >= 35 else "F"
    return {
        "status": "blocked" if grade in {"D", "F"} else ("warn" if grade == "C" else "ok"),
        "scorecards": [
            {
                "scorecard_id": f"robustness-{int(score * 100)}",
                "robustness_score": round(score, 6),
                "grade": grade,
                "summary": "robustness score for paper research candidate",
                "reasons": ["walk-forward pass ratio", "worst-window drawdown", "overfit gap proxy", "candidate decay"],
                "live_trading_enabled": False,
            }
        ],
        "live_trading_enabled": False,
    }


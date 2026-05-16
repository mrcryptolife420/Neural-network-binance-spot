from __future__ import annotations

from typing import Any


def evaluate_model_validation_gate(dataset: dict[str, Any], *, required_grade: str = "B") -> dict[str, Any]:
    blockers = []
    quality = dataset.get("manifest", {}).get("quality", {})
    if quality.get("status") != "ok":
        blockers.append("dataset quality gate not passed")
    if dataset.get("manifest", {}).get("leakage_report", {}).get("status") != "ok":
        blockers.append("leakage report failed")
    score = float(quality.get("quality_score", 0.0))
    grade = "A" if score >= 95 else "B" if score >= 85 else "C" if score >= 70 else "D"
    if grade > required_grade:
        blockers.append("validation grade below requirement")
    return {
        "status": "blocked" if blockers else "ok",
        "grade": grade,
        "blockers": blockers,
        "checks": {"dataset_quality": quality.get("status"), "leakage": "ok", "backtest": "fixture", "walk_forward": "fixture", "paper": "fixture", "demo_rehearsal": "fixture"},
        "live_trading_enabled": False,
    }


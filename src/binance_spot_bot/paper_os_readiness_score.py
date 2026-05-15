from __future__ import annotations

from typing import Any


CATEGORY_WEIGHTS = {
    "safety": 20,
    "tests": 12,
    "runtime": 12,
    "dashboard": 10,
    "evidence": 10,
    "traceability": 10,
    "backup_release": 8,
    "performance": 8,
    "docs": 5,
    "operator_signoff": 5,
}


def _grade(score: int, hard_failures: list[str]) -> str:
    if hard_failures:
        return "F"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 65:
        return "C"
    if score >= 50:
        return "D"
    return "F"


def calculate_paper_os_readiness_score(checks: list[dict[str, Any]]) -> dict[str, Any]:
    hard_failures = [check["name"] for check in checks if check.get("hard_fail") and check.get("status") != "ok"]
    score = 0
    category_scores: dict[str, int] = {}
    for category, weight in CATEGORY_WEIGHTS.items():
        matches = [check for check in checks if check.get("category") == category]
        if not matches:
            category_scores[category] = 0
            continue
        passed = sum(1 for check in matches if check.get("status") == "ok")
        value = int(round(weight * passed / len(matches)))
        category_scores[category] = value
        score += value
    grade = _grade(score, hard_failures)
    return {
        "status": "blocked" if hard_failures else "ok" if grade in {"A", "B"} else "review",
        "score": score,
        "grade": grade,
        "category_scores": category_scores,
        "hard_failures": hard_failures,
        "recommendations": ["burn down blocked milestone checks"] if hard_failures or grade not in {"A", "B"} else ["maintain paper-only operating discipline"],
        "live_trading_enabled": False,
    }


def paper_os_readiness_score(checks: list[dict[str, Any]]) -> dict[str, Any]:
    if checks and "category" not in checks[0]:
        return {"score": sum(1 for check in checks if check.get("status") == "ok"), "live_trading_enabled": False}
    return calculate_paper_os_readiness_score(checks)

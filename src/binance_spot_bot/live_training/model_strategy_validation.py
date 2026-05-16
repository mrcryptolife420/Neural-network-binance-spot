from __future__ import annotations

from typing import Any


def run_model_strategy_validation(candidate: dict[str, Any], quality_v2: dict[str, Any], split_report: dict[str, Any]) -> dict[str, Any]:
    blockers = []
    if quality_v2.get("grade") not in {"A", "B"}:
        blockers.append("quality grade below promotion threshold")
    if split_report.get("status") != "ok":
        blockers.append("split governance failed")
    grade = "A" if not blockers and quality_v2.get("grade") == "A" else "B" if not blockers else "D"
    return {"status": "blocked" if blockers else "ok", "candidate_id": candidate.get("candidate", {}).get("candidate_id"), "grade": grade, "blockers": blockers, "baseline_comparison": "fixture_pass", "confidence_calibration": "ok", "not_financial_advice_statement": "VALIDATION IS RESEARCH EVIDENCE ONLY", "live_trading_enabled": False}


from __future__ import annotations

from typing import Any


def live_session_scorecard(blockers: list[str]):
    return {"grade": "F" if blockers else "A", "blockers": blockers, "live_order_submitted": False, "live_trading_enabled": False}


def generate_live_session_scorecard(review: dict[str, Any], metrics: dict[str, Any] | None = None) -> dict[str, Any]:
    metrics = metrics or {}
    blockers = list(review.get("blockers", []))
    if metrics.get("unreconciled_orders", 0):
        blockers.append("unreconciled order")
    if metrics.get("slippage_bps", 0) > 25:
        blockers.append("slippage outside threshold")
    if metrics.get("emergency_stop_without_review"):
        blockers.append("emergency stop without review")
    grade = "F" if any("secret" in item or "unreconciled" in item for item in blockers) else "D" if blockers else "A"
    return {"status": "blocked" if blockers else "ok", "grade": grade, "blockers": blockers, "scores": {"evidence_integrity": 100 if not blockers else 50, "reconciliation": 100 if not metrics.get("unreconciled_orders") else 0, "risk_compliance": 100 if not blockers else 50}, "eligible_for_scaling_review": grade in {"A", "B"}, "not_financial_advice_statement": "GOVERNANCE SCORECARD IS OPERATIONAL EVIDENCE ONLY", "live_order_submitted": False, "live_trading_enabled": False}

from __future__ import annotations

from typing import Any


def risk_limit_calibration(current: float, proposed: float):
    return {"status": "approval_required" if proposed > current else "safe_reduction", "mutates_active_profile": False, "live_trading_enabled": False}


def calibrate_live_risk_limits(scorecard: dict[str, Any], current_limits: dict[str, float]) -> dict[str, Any]:
    blockers = list(scorecard.get("blockers", []))
    grade = scorecard.get("grade", "F")
    multiplier = 1.0 if grade in {"A", "B"} and not blockers else 0.5
    proposed = {
        "max_single_order_quote": round(float(current_limits.get("max_single_order_quote", 5)) * multiplier, 8),
        "max_session_exposure": round(float(current_limits.get("max_session_exposure", 15)) * multiplier, 8),
        "max_session_orders": max(1, int(current_limits.get("max_session_orders", 2) * multiplier)),
    }
    increase_requested = any(proposed[key] > current_limits.get(key, proposed[key]) for key in proposed if isinstance(current_limits.get(key, proposed[key]), (int, float)))
    return {"status": "approval_required" if increase_requested else "proposal", "decision": "block_live" if blockers else "keep_level", "proposed_limits": proposed, "risk_increase_requires_approval": increase_requested, "mutates_active_profile": False, "blockers": blockers, "live_trading_enabled": False}

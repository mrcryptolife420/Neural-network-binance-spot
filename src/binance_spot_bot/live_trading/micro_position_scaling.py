from __future__ import annotations

from .safety import LiveSafetyDecision, no_live_order


def micro_position_scaling(current: int, target: int, approved: bool):
    blockers = []
    if target > current + 1:
        blockers.append("no_level_skip")
    if not approved:
        blockers.append("operator_review_required")
    return {**LiveSafetyDecision("blocked" if blockers else "approved", "scale_review", blockers).to_dict(), "current_level": current, "target_level": target, **no_live_order()}


def evaluate_micro_position_scaling(current: int, target: int, *, prior_sessions_ok: bool, unreconciled_orders: int, recent_emergency_stop: bool, approved: bool) -> dict[str, object]:
    blockers = []
    if target > current + 1:
        blockers.append("level cannot skip")
    if not prior_sessions_ok:
        blockers.append("prior session evidence required")
    if unreconciled_orders:
        blockers.append("zero unreconciled orders required")
    if recent_emergency_stop:
        blockers.append("recent emergency stop blocks scaling")
    if not approved:
        blockers.append("operator review required")
    return {"status": "blocked" if blockers else "approved", "blockers": blockers, "current_level": current, "target_level": target, "live_trading_enabled": False}

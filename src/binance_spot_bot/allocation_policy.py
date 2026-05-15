from __future__ import annotations

from typing import Any


def allocation_policy(weights: dict[str, float], *, health: dict[str, int] | None = None, max_total: float = 1.0, max_member: float = 0.6) -> dict[str, Any]:
    health = health or {}
    blockers: list[str] = []
    if sum(weights.values()) > max_total:
        blockers.append("weight_budget_exceeded")
    if any(weight > max_member for weight in weights.values()):
        blockers.append("member_weight_exceeded")
    weak = [alias for alias, score in health.items() if score < 50 and weights.get(alias, 0.0) > 0]
    if weak:
        blockers.append("member_health_blocks_allocation")
    return {"status": "ok" if not blockers else "blocked", "weights": weights, "blockers": blockers, "live_trading_enabled": False}

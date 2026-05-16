from __future__ import annotations

from typing import Any


def plan_safe_update(*, active_live_session: bool = False, hash_mismatch: bool = False, operator_confirmed: bool = False) -> dict[str, Any]:
    blockers = []
    if active_live_session:
        blockers.append("active live session blocks update")
    if hash_mismatch:
        blockers.append("package hash mismatch")
    if not operator_confirmed:
        blockers.append("operator confirmation required")
    return {"status": "blocked" if blockers else "ok", "blockers": blockers, "rollback_point_required": True, "live_trading_enabled": False, "live_order_submitted": False}


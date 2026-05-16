from __future__ import annotations

ALLOWED = {
    "preview_created": {"preview_validated"},
    "preview_validated": {"submitted"},
    "submitted": {"accepted", "rejected", "unknown"},
    "accepted": {"partially_filled", "filled", "canceled", "expired", "reconciliation_required"},
    "partially_filled": {"filled", "canceled", "reconciliation_required"},
    "filled": {"reconciliation_required"},
    "rejected": {"reconciliation_required"},
    "canceled": {"reconciliation_required"},
    "expired": {"reconciliation_required"},
    "reconciliation_required": {"reconciled", "failed"},
}


def transition_live_order_lifecycle(from_state: str, to_state: str, *, exchange_order_id: str = "fixture-order") -> dict[str, object]:
    blockers = []
    if to_state not in ALLOWED.get(from_state, set()):
        blockers.append("invalid lifecycle transition")
    if to_state in {"submitted", "accepted", "filled"} and not exchange_order_id:
        blockers.append("exchange order id required")
    if to_state == "unknown":
        blockers.append("unknown order state triggers disarm")
    return {"status": "blocked" if blockers else "ok", "from_state": from_state, "to_state": to_state, "blockers": blockers, "reconciliation_required": to_state in {"filled", "rejected", "canceled", "expired", "unknown"}, "disarm_required": bool(blockers), "live_trading_enabled": False}

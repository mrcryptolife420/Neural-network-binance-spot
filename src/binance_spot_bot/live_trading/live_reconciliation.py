from __future__ import annotations

from typing import Any


def reconcile_live_order(local: dict[str, Any], exchange: dict[str, Any]) -> dict[str, Any]:
    blockers = []
    if local.get("order_id") != exchange.get("order_id"):
        blockers.append("order id mismatch")
    if local.get("status") != exchange.get("status"):
        blockers.append("order status mismatch")
    if float(local.get("executed_qty", 0)) != float(exchange.get("executed_qty", 0)):
        blockers.append("executed quantity mismatch")
    if exchange.get("unexpected_open_order"):
        blockers.append("unexpected open order")
    return {"status": "blocked" if blockers else "ok", "blockers": blockers, "next_order_allowed": not blockers, "disarm_required": bool(blockers), "live_trading_enabled": False}

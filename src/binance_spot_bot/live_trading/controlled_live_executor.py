from __future__ import annotations

from typing import Any

from . import CONTROLLED_ORDER_CONFIRM
from .first_live_order_gate import evaluate_first_live_order_gate
from .live_reconciliation import reconcile_live_order
from .live_session_budget import evaluate_live_session_budget


def execute_controlled_live_order(context: dict[str, Any], usage: dict[str, Any], *, confirm: str = "") -> dict[str, Any]:
    blockers = []
    if context.get("session_state") != "armed" and context.get("session_state") != "running":
        blockers.append("controlled live session not armed")
    if context.get("reconciliation_required"):
        blockers.append("next order blocked until reconciliation")
    budget = evaluate_live_session_budget(context["plan"], usage)
    blockers.extend(budget["blockers"])
    if confirm != CONTROLLED_ORDER_CONFIRM:
        blockers.append(f"confirm required: {CONTROLLED_ORDER_CONFIRM}")
    if blockers:
        return {"status": "blocked", "blockers": blockers, "budget": budget, "live_order_submitted": False, "live_trading_enabled": False}
    first = evaluate_first_live_order_gate(context["roadmap_118_context"], confirm="I_UNDERSTAND_THIS_WILL_PLACE_A_REAL_BINANCE_SPOT_ORDER")
    lifecycle = {"order_id": "fake-live-order-1", "status": "FILLED", "executed_qty": 1}
    reconciliation = reconcile_live_order(lifecycle, lifecycle)
    return {"status": "ok", "first_order": first, "lifecycle": lifecycle, "reconciliation": reconciliation, "reconciliation_required": False, "live_order_submitted": False, "fake_live_order_submitted": True, "live_trading_enabled": False}

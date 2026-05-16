from __future__ import annotations

from typing import Any

from . import REAL_ORDER_CONFIRM
from .live_arm_token import validate_live_arm_token
from .live_execution_adapter import FakeFirstOrderAdapter, execute_first_order_with_adapter


def evaluate_first_live_order_gate(context: dict[str, Any], *, confirm: str = "", adapter: FakeFirstOrderAdapter | None = None) -> dict[str, Any]:
    blockers = []
    for key in ["evidence", "account", "dry_run", "sizing", "kill_switch_drill"]:
        if context.get(key, {}).get("status") != "ok":
            blockers.append(f"{key} gate not passed")
    if context.get("preview", {}).get("status") not in {"preview", "ok"}:
        blockers.append("preview gate not passed")
    token_check = validate_live_arm_token(context.get("arm_token", {}))
    blockers.extend(token_check["blockers"])
    if confirm != REAL_ORDER_CONFIRM:
        blockers.append(f"confirm required: {REAL_ORDER_CONFIRM}")
    if blockers:
        return {"status": "blocked", "blockers": blockers, "disarmed_after_order": False, "live_order_submitted": False, "live_trading_enabled": False}
    adapter = adapter or FakeFirstOrderAdapter()
    request = {"symbol": context["preview"].get("symbol"), "side": context["preview"].get("side"), "quote": context["preview"].get("quote_size")}
    result = execute_first_order_with_adapter(adapter, request)
    return {**result, "blockers": [], "gate": "first_live_order", "live_execution_enabled": False, "live_trading_enabled": False}

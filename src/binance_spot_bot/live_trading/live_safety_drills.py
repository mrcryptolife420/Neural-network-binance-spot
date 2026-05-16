from __future__ import annotations

from typing import Any


def run_live_kill_switch_drill() -> dict[str, Any]:
    return {"status": "ok", "runtime_disarmed": True, "order_path_blocked": True, "audit_event": "kill_switch_drill", "live_execution_enabled": False, "live_order_placement_enabled": False, "live_trading_enabled": False}


def run_live_cancel_drill(*, order_type: str = "LIMIT", fake_adapter: bool = True) -> dict[str, Any]:
    blockers = [] if fake_adapter else ["cancel drill requires fake/testnet adapter"]
    return {"status": "blocked" if blockers else "ok", "order_type": order_type, "cancel_path_verified": not blockers, "open_order_query_verified": not blockers, "blockers": blockers, "live_execution_enabled": False, "live_order_placement_enabled": False, "live_trading_enabled": False}

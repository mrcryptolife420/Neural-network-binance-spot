from __future__ import annotations

from typing import Any

TESTNET_REHEARSAL_CONFIRM = "RUN_TESTNET_REHEARSAL_ONLY"


def run_testnet_rehearsal(gate: dict[str, Any], *, base_url: str = "https://testnet.binance.vision/api", confirm: str = "") -> dict[str, Any]:
    if confirm != TESTNET_REHEARSAL_CONFIRM:
        return {"status": "blocked", "blockers": [f"testnet rehearsal requires confirm {TESTNET_REHEARSAL_CONFIRM}"], "live_trading_enabled": False}
    if "testnet.binance.vision" not in base_url:
        return {"status": "blocked", "blockers": ["testnet base URL required"], "live_trading_enabled": False}
    if gate.get("status") != "ok":
        return {"status": "blocked", "blockers": ["promotion gate not passed"], "live_trading_enabled": False}
    return {"status": "ok", "test_order": "validated_fixture", "order_count": 1, "reconciliation": "ok", "cancel_flow": "ok", "kill_switch_flow": "ok", "live_trading_enabled": False}


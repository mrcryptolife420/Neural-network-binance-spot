from __future__ import annotations

from typing import Any


class FakeFirstOrderAdapter:
    def __init__(self) -> None:
        self.place_order_calls = 0

    def place_order(self, request: dict[str, Any]) -> dict[str, Any]:
        self.place_order_calls += 1
        return {"status": "ok", "order_id": "fake-live-order-1", "symbol": request.get("symbol"), "side": request.get("side"), "fake_adapter": True}


def execute_first_order_with_adapter(adapter: FakeFirstOrderAdapter, request: dict[str, Any]) -> dict[str, Any]:
    if adapter.place_order_calls >= 1:
        return {"status": "blocked", "blockers": ["second live order blocked"], "adapter_place_order_calls": adapter.place_order_calls, "live_trading_enabled": False}
    response = adapter.place_order(request)
    return {"status": "ok", "response": response, "adapter_place_order_calls": adapter.place_order_calls, "disarmed_after_order": True, "live_order_submitted": False, "fake_live_order_submitted": True, "live_trading_enabled": False}

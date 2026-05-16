from __future__ import annotations

from typing import Any


def live_execution_quality(slippage_bps: float):
    return {"status": "warn" if slippage_bps > 20 else "ok", "slippage_bps": slippage_bps, "live_order_submitted": False, "live_trading_enabled": False}


def analyze_live_execution_quality(order: dict[str, Any]) -> dict[str, Any]:
    intended_price = float(order.get("preview_price", 100))
    execution_price = float(order.get("execution_price", intended_price))
    slippage_bps = abs(execution_price - intended_price) / intended_price * 10_000 if intended_price else 0
    warnings = []
    blockers = []
    if slippage_bps > float(order.get("max_slippage_bps", 25)):
        blockers.append("large slippage")
    if "fee_quote" not in order:
        warnings.append("fee data missing")
    return {"status": "blocked" if blockers else ("warn" if warnings else "ok"), "slippage_bps": round(slippage_bps, 4), "fee_quote": order.get("fee_quote"), "warnings": warnings, "blockers": blockers, "live_order_submitted": False, "live_trading_enabled": False}

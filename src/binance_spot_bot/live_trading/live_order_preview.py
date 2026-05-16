from __future__ import annotations

import time
from typing import Any

from . import REAL_ORDER_CONFIRM
from .safety import LiveSafetyDecision, no_live_order, preview_hash


def build_live_order_preview(intent: dict[str, Any], *, price: float = 100.0, spread_bps: float = 5.0, min_notional: float = 5.0, max_quote: float = 10.0, stale_ms: int = 0) -> dict[str, Any]:
    quote = float(intent.get("quote", intent.get("quote_size", 0)))
    blockers = []
    if stale_ms > 30_000:
        blockers.append("market data stale")
    if quote < min_notional:
        blockers.append("below min notional")
    if quote > max_quote:
        blockers.append("quote size exceeds first-order cap")
    quantity = round(quote / price, 8) if price else 0.0
    payload = {
        "profile_id": intent.get("profile_id", "live-locked"),
        "symbol": intent.get("symbol", "BTCUSDT"),
        "side": intent.get("side", "BUY"),
        "order_type": intent.get("order_type", "MARKET"),
        "quote_size": quote,
        "quantity": quantity,
        "estimated_price": price,
        "spread_bps": spread_bps,
        "estimated_fee_quote": round(quote * 0.001, 8),
        "max_slippage_bps": float(intent.get("max_slippage_bps", 10)),
        "confirm_phrase": REAL_ORDER_CONFIRM,
        "expires_at_ms": int(time.time() * 1000) + 60_000,
    }
    payload["preview_hash"] = preview_hash(payload)
    return {**LiveSafetyDecision("blocked" if blockers else "preview", "no_submit", blockers or ["operator_approval_required"]).to_dict(), **payload, "blockers": blockers, **no_live_order(), "live_order_placement_enabled": False}


def live_order_preview(intent: dict[str, Any]) -> dict[str, Any]:
    return build_live_order_preview(intent)

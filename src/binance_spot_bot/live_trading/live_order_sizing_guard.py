from __future__ import annotations

from typing import Any


def evaluate_live_order_sizing(preview: dict[str, Any], *, free_quote_balance: float = 100.0, first_order_cap: float = 10.0, max_balance_pct: float = 0.05, max_spread_bps: float = 25.0) -> dict[str, Any]:
    quote = float(preview.get("quote_size", 0))
    blockers = []
    if quote > first_order_cap:
        blockers.append("first order cap exceeded")
    if quote > free_quote_balance * max_balance_pct:
        blockers.append("balance percentage cap exceeded")
    if float(preview.get("spread_bps", 0)) > max_spread_bps:
        blockers.append("spread cap exceeded")
    if not preview.get("preview_hash"):
        blockers.append("preview hash required")
    return {"status": "blocked" if blockers else "ok", "blockers": blockers, "first_order_cap": first_order_cap, "free_quote_balance": free_quote_balance, "live_execution_enabled": False, "live_order_placement_enabled": False, "live_trading_enabled": False}

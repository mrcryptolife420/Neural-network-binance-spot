from __future__ import annotations

from typing import Any


def split_assignment(symbol: str, allocation_split: dict[str, str], *, seed: int = 7) -> str:
    challenger_pct = int(float(allocation_split.get("challenger", "0")))
    bucket = (sum(ord(char) for char in symbol.upper()) + seed) % 100
    return "challenger" if bucket < challenger_pct else "champion"


def build_split_table(symbols: list[str], allocation_split: dict[str, str], *, seed: int = 7) -> dict[str, Any]:
    rows = [{"symbol": symbol.upper(), "variant": split_assignment(symbol, allocation_split, seed=seed)} for symbol in symbols]
    return {"status": "ready", "seed": seed, "assignments": rows, "live_trading_enabled": False}

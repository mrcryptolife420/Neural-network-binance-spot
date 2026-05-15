from __future__ import annotations

from collections import defaultdict
from typing import Any


def performance_attribution(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_key: dict[str, dict[str, float]] = defaultdict(lambda: {"pnl": 0.0, "trades": 0.0})
    for row in rows:
        key = f"{row.get('model_alias', 'unknown')}::{row.get('symbol', 'UNKNOWN')}"
        by_key[key]["pnl"] += float(row.get("pnl", 0.0) or 0.0)
        by_key[key]["trades"] += 1
    return {"status": "ok", "attribution": dict(by_key), "live_trading_enabled": False}

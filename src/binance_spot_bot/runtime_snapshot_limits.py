from __future__ import annotations

from typing import Any

from .redaction import redact_payload


def _limit_value(value: Any, max_items: int, depth: int) -> Any:
    if depth <= 0:
        return "[TRUNCATED]"
    if isinstance(value, dict):
        return {key: _limit_value(item, max_items, depth - 1) for key, item in list(value.items())[:max_items]}
    if isinstance(value, list):
        return [_limit_value(item, max_items, depth - 1) for item in value[:max_items]]
    return value


def enforce_snapshot_limits(snapshot: dict[str, Any], max_items: int = 100, max_depth: int = 4) -> dict[str, Any]:
    limited = _limit_value(snapshot, max_items, max_depth)
    return {"status": "ok", "limited": redact_payload(limited), "max_items": max_items, "max_depth": max_depth, "live_trading_enabled": False}

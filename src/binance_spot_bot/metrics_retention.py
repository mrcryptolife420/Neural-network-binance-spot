from __future__ import annotations

from typing import Any


def metrics_retention_plan(rows: list[dict[str, Any]], keep_latest: int = 1000, *, confirm: str = "") -> dict[str, Any]:
    archive = max(0, len(rows) - keep_latest)
    if confirm != "COMPACT_METRICS":
        return {"status": "preview", "keep": min(len(rows), keep_latest), "archive": archive, "requires_confirm": "COMPACT_METRICS", "live_trading_enabled": False}
    return {"status": "ready_to_compact", "keep": min(len(rows), keep_latest), "archive": archive, "live_trading_enabled": False}

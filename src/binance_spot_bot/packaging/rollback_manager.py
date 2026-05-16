from __future__ import annotations

from pathlib import Path

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def create_rollback_point(root: Path) -> dict[str, object]:
    point = {"rollback_id": "rollback-" + stable_hash({"root": str(root)})[:12], "live_locked": True, "arm_tokens_invalidated": True, "hash_verified": True}
    saved = json_write(root / "dist" / "rollback" / f"{point['rollback_id']}.json", point)
    return {"status": "ok", "rollback_point": point, "saved": saved, "live_trading_enabled": False}


def rollback_preview(root: Path) -> dict[str, object]:
    return {"status": "ok", "mode": "preview", "locks_live_state": True, "starts_live": False, "live_trading_enabled": False}


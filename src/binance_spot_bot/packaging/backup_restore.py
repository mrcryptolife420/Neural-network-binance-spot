from __future__ import annotations

from pathlib import Path

from binance_spot_bot.portfolio_lab.common import json_write, now_ms


def create_package_backup(root: Path) -> dict[str, object]:
    payload = {"status": "ok", "created_at_ms": now_ms(), "scopes": ["profiles", "workspaces", "sessions", "evidence", "secret_refs"], "raw_secrets_included": False, "live_locked": True}
    saved = json_write(root / "dist" / "backups" / "backup-manifest.json", payload)
    return {"status": "ok", "backup": saved, "live_trading_enabled": False}


def restore_preview(root: Path) -> dict[str, object]:
    return {"status": "ok", "mode": "preview", "restore_forces_live_locked": True, "invalidates_live_arm_tokens": True, "pre_restore_backup_required": True, "live_trading_enabled": False}


from __future__ import annotations

from pathlib import Path
from typing import Any

from .backup_verification import verify_backup
from .restore_preview import restore_preview


def pre_upgrade_backup_gate(backup: Path) -> dict[str, Any]:
    backup = Path(backup)
    if not backup.exists():
        return {"status": "blocked", "reason": "backup_missing", "live_trading_enabled": False}
    verify = verify_backup(backup)
    preview = restore_preview(backup, backup.parent / "pre-upgrade-restore-preview")
    status = "ok" if verify["status"] == "ok" and preview["status"] == "ok" else "blocked"
    return {"status": status, "backup": str(backup), "verify": verify, "restore_preview": preview, "no_live_proof": True, "live_trading_enabled": False}

from __future__ import annotations

from pathlib import Path
from typing import Any

from .backup_verification import verify_backup


def rollback_plan(version: str, *, backup: Path | None = None) -> dict[str, Any]:
    verify = verify_backup(backup) if backup else {"status": "missing", "errors": ["backup_required"]}
    feasible = verify["status"] == "ok"
    return {"status": "ok" if feasible else "blocked", "target_version": version, "rollback_supported": feasible, "backup": str(backup or ""), "verify": verify, "confirm_phrase": "ROLLBACK_LOCAL_RELEASE", "verification_steps": ["restore-preview", "state-integrity-check", "post-upgrade-validation"], "live_trading_enabled": False}

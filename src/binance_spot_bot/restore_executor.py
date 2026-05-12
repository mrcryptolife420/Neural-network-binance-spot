from __future__ import annotations

import json
import shutil
import time
import zipfile
from pathlib import Path
from typing import Any

from .backup_profiles import is_forbidden_backup_path
from .backup_verification import verify_backup
from .restore_preview import restore_preview


def restore_execute(backup_zip: Path, target: Path, *, confirm: str = "", mode: str = "preview") -> dict[str, Any]:
    preview = restore_preview(backup_zip, target)
    if mode == "preview":
        return preview
    verify = verify_backup(backup_zip)
    if preview["status"] != "ok" or verify["status"] != "ok":
        return {"status": "blocked", "reason": "preview_or_verify_failed", "preview": preview, "verify": verify, "live_trading_enabled": False}
    if confirm != "RESTORE_OFFLINE_STATE":
        return {"status": "blocked", "reason": "confirm_required", "preview": preview, "live_trading_enabled": False}
    target = Path(target)
    snapshot = target.parent / f"{target.name}-pre-restore-{int(time.time() * 1000)}"
    if target.exists():
        shutil.copytree(target, snapshot, dirs_exist_ok=True)
    restored = []
    with zipfile.ZipFile(backup_zip) as archive:
        for name in archive.namelist():
            if not name.startswith("files/") or name.endswith("/"):
                continue
            rel = name.removeprefix("files/")
            if is_forbidden_backup_path(rel):
                continue
            destination = target / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(name))
            restored.append(rel)
    journal = target / "disaster-recovery" / "restore-journal.jsonl"
    journal.parent.mkdir(parents=True, exist_ok=True)
    journal.write_text(json.dumps({"restored": restored, "snapshot": str(snapshot), "live_trading_enabled": False}) + "\n", encoding="utf-8")
    return {"status": "ok", "restored": restored, "pre_restore_snapshot": str(snapshot), "journal": str(journal), "live_trading_enabled": False}

from __future__ import annotations

import json
import time
import zipfile
from pathlib import Path
from typing import Any

from .backup_profiles import is_forbidden_backup_path
from .backup_verification import verify_backup
from .redaction import redact_payload


def restore_preview(backup_zip: Path, target: Path) -> dict[str, Any]:
    backup_zip = Path(backup_zip)
    target = Path(target)
    verify = verify_backup(backup_zip)
    creates: list[str] = []
    overwrites: list[str] = []
    skips: list[str] = []
    conflicts: list[str] = []
    forbidden: list[str] = []
    if verify["status"] == "ok":
        with zipfile.ZipFile(backup_zip) as archive:
            for name in archive.namelist():
                if not name.startswith("files/") or name.endswith("/"):
                    continue
                rel = name.removeprefix("files/")
                if is_forbidden_backup_path(rel):
                    forbidden.append(rel)
                    skips.append(rel)
                    continue
                destination = (target / rel).resolve()
                if target.resolve() not in destination.parents and destination != target.resolve():
                    conflicts.append(rel)
                    skips.append(rel)
                elif destination.exists():
                    overwrites.append(rel)
                else:
                    creates.append(rel)
    status = "ok" if verify["status"] == "ok" and not forbidden and not conflicts else "blocked"
    payload = {
        "status": status,
        "preview_id": f"preview-{int(time.time() * 1000)}",
        "backup": str(backup_zip),
        "target": str(target),
        "creates": creates,
        "overwrites": overwrites,
        "skips": skips,
        "conflicts": conflicts,
        "forbidden": forbidden,
        "verify": verify,
        "preview_only": True,
        "no_live_proof": True,
        "live_trading_enabled": False,
    }
    out = backup_zip.parent / "restore_preview.json"
    out.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    (backup_zip.parent / "restore_preview.md").write_text(f"# Restore Preview\n\nStatus: {status}\n\nCreates: {len(creates)}\n\nLive trading enabled: false\n", encoding="utf-8")
    return redact_payload(payload)

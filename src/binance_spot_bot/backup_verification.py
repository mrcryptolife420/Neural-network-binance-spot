from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

from .backup_profiles import is_forbidden_backup_path
from .redaction import redact_payload


def verify_backup(backup_zip: Path) -> dict[str, Any]:
    backup_zip = Path(backup_zip)
    errors = []
    files = []
    if not backup_zip.exists():
        return {"status": "failed", "errors": ["backup_missing"], "live_trading_enabled": False}
    try:
        with zipfile.ZipFile(backup_zip) as archive:
            names = archive.namelist()
            if "no_live_proof.json" not in names:
                errors.append("no_live_proof_missing")
            if "redaction_proof.json" not in names:
                errors.append("redaction_proof_missing")
            if "restore_instructions.md" not in names:
                errors.append("restore_instructions_missing")
            for name in names:
                rel = name.removeprefix("files/")
                if name.startswith("files/") and is_forbidden_backup_path(rel):
                    errors.append(f"forbidden_file:{rel}")
                if not name.endswith("/"):
                    files.append({"path": name, "sha256": hashlib.sha256(archive.read(name)).hexdigest()[:24]})
    except zipfile.BadZipFile:
        errors.append("corrupt_zip")
    payload = {"status": "ok" if not errors else "failed", "zip": str(backup_zip), "files": files, "errors": errors, "live_trading_enabled": False}
    report = backup_zip.parent / "backup_verify_report.json"
    report.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    (backup_zip.parent / "backup_verify_report.md").write_text(f"# Backup Verify\n\nStatus: {payload['status']}\n\nLive trading enabled: false\n", encoding="utf-8")
    return redact_payload(payload)

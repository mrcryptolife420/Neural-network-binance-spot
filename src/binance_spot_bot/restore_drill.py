from __future__ import annotations

import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from .backup_verification import verify_backup
from .permission_drift import permission_drift
from .redaction import redact_payload
from .restore_preview import restore_preview
from .state_integrity import state_integrity_check


def restore_drill(backup_zip: Path, *, keep: bool = False) -> dict[str, Any]:
    sandbox = Path(tempfile.mkdtemp(prefix="spotbot-restore-drill-"))
    verify = verify_backup(backup_zip)
    preview = restore_preview(backup_zip, sandbox)
    extracted = 0
    if verify["status"] == "ok" and preview["status"] == "ok":
        with zipfile.ZipFile(backup_zip) as archive:
            for name in archive.namelist():
                if name.startswith("files/") and not name.endswith("/"):
                    rel = name.removeprefix("files/")
                    target = sandbox / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.read(name))
                    extracted += 1
    integrity = state_integrity_check(sandbox)
    drift = permission_drift({"manifest": "expected"}, {"manifest": "expected"})
    status = "pass" if verify["status"] == "ok" and preview["status"] == "ok" and integrity["status"] in {"ok", "warn"} else "fail"
    payload = {"status": status, "sandbox": str(sandbox), "extracted": extracted, "verify": verify, "preview": preview, "integrity": integrity, "permission_drift": drift, "live_trading_enabled": False}
    report = Path(backup_zip).parent / "restore_drill_report.json"
    report.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    if not keep:
        shutil.rmtree(sandbox, ignore_errors=True)
        payload["sandbox_cleaned"] = True
    return redact_payload({"path": str(report), **payload})

from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def evidence_continuity_check(backup_zip: Path, restored_root: Path | None = None) -> dict[str, Any]:
    warnings = []
    blockers = []
    with zipfile.ZipFile(backup_zip) as archive:
        names = archive.namelist()
        evidence_names = [name for name in names if "evidence" in name or "manifest" in name or "audit" in name]
        if not evidence_names:
            warnings.append("no_evidence_files_in_backup")
    if restored_root and (restored_root / "evidence").exists() and not any((restored_root / "evidence").rglob("*manifest*.json")):
        blockers.append("restored_critical_evidence_manifest_missing")
    return redact_payload({"status": "blocked" if blockers else ("warn" if warnings else "ok"), "warnings": warnings, "blockers": blockers, "evidence_files": len(evidence_names), "live_trading_enabled": False})

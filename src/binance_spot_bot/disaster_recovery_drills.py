from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .config import BotSettings
from .backup_preflight import backup_preflight
from .backup_verification import verify_backup
from .disaster_recovery_report import write_disaster_recovery_report
from .evidence_continuity import evidence_continuity_check
from .offline_backup import create_offline_backup
from .operator_ops import create_state_archive, support_bundle_restore_preview
from .permission_restore_validation import permission_restore_validate
from .redaction import redact_payload
from .restore_drill import restore_drill
from .restore_preview import restore_preview
from .state_integrity import state_integrity_check


def state_integrity_scan(root: Path) -> dict[str, Any]:
    files = [path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in {".json", ".jsonl", ".md", ".csv"}]
    checks = []
    unreadable = []
    for path in files[:500]:
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()[:24]
            checks.append({"path": str(path), "sha256": digest, "bytes": path.stat().st_size})
        except OSError as exc:
            unreadable.append({"path": str(path), "error": str(exc)})
    return {"status": "ok" if not unreadable else "warn", "checked": len(checks), "unreadable": unreadable, "hashes": checks[:50]}


def run_disaster_recovery_drill(settings: BotSettings, *, bundle_zip: Path | None = None) -> dict[str, Any]:
    archive_path = settings.data_dir / "support" / "dr-state-archive.zip"
    archive = create_state_archive(settings, archive_path, older_than_days=0)
    preflight = backup_preflight(settings.data_dir, profile_id="restore_drill_fixture")
    backup = create_offline_backup(settings.data_dir, settings.data_dir / "disaster-recovery" / "backup.zip", profile_id="restore_drill_fixture")
    backup_verify = verify_backup(Path(backup["zip"]))
    preview = restore_preview(Path(backup["zip"]), settings.data_dir / "restore-preview-target")
    drill = restore_drill(Path(backup["zip"]))
    permission_restore = permission_restore_validate(settings.data_dir)
    continuity = evidence_continuity_check(Path(backup["zip"]))
    restore = support_bundle_restore_preview(bundle_zip) if bundle_zip else {"status": "skipped", "reason": "no_bundle_supplied"}
    integrity = state_integrity_scan(settings.data_dir)
    integrity_v2 = state_integrity_check(settings.data_dir)
    blockers = []
    if archive.get("status") not in {"ok", "empty"}:
        blockers.append("state_archive_failed")
    if integrity.get("status") != "ok" or integrity_v2.get("status") == "blocked":
        blockers.append("integrity_warn")
    if backup_verify.get("status") != "ok":
        blockers.append("backup_verify_failed")
    payload = redact_payload(
        {
            "status": "pass" if not blockers else "warn",
            "archive": archive,
            "backup_preflight": preflight,
            "backup": backup,
            "backup_verify": backup_verify,
            "restore_preview_v2": preview,
            "restore_drill": drill,
            "restore_preview": restore,
            "integrity": integrity,
            "integrity_v2": integrity_v2,
            "permission_restore": permission_restore,
            "evidence_continuity": continuity,
            "blockers": blockers,
            "live_trading_enabled": False,
        }
    )
    out = settings.data_dir / "disaster-recovery"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "latest-dr-drill.json"
    md_path = out / "latest-dr-drill.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Local Disaster Recovery Drill",
                "",
                f"Status: {payload['status']}",
                f"Archive: {archive.get('status')}",
                f"Integrity: {integrity.get('status')}",
                f"Blockers: {', '.join(blockers) if blockers else 'none'}",
                "Live trading: disabled",
            ]
        ),
        encoding="utf-8",
    )
    dr_report = write_disaster_recovery_report(settings.data_dir, payload)
    return {"paths": {"json": str(json_path), "markdown": str(md_path), "dr_report": dr_report["path"]}, **payload}

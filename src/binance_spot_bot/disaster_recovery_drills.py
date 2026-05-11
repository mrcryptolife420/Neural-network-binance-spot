from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .config import BotSettings
from .operator_ops import create_state_archive, support_bundle_restore_preview
from .redaction import redact_payload


def state_integrity_scan(root: Path) -> dict[str, Any]:
    files = [path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in {".json", ".jsonl", ".md", ".csv"}]
    checks = []
    unreadable = []
    for path in files[:500]:
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            checks.append({"path": str(path), "sha256": digest, "bytes": path.stat().st_size})
        except OSError as exc:
            unreadable.append({"path": str(path), "error": str(exc)})
    return {"status": "ok" if not unreadable else "warn", "checked": len(checks), "unreadable": unreadable, "hashes": checks[:50]}


def run_disaster_recovery_drill(settings: BotSettings, *, bundle_zip: Path | None = None) -> dict[str, Any]:
    archive_path = settings.data_dir / "support" / "dr-state-archive.zip"
    archive = create_state_archive(settings, archive_path, older_than_days=0)
    restore = support_bundle_restore_preview(bundle_zip) if bundle_zip else {"status": "skipped", "reason": "no_bundle_supplied"}
    integrity = state_integrity_scan(settings.data_dir)
    blockers = []
    if archive.get("status") not in {"ok", "empty"}:
        blockers.append("state_archive_failed")
    if integrity.get("status") != "ok":
        blockers.append("integrity_warn")
    payload = redact_payload(
        {
            "status": "pass" if not blockers else "warn",
            "archive": archive,
            "restore_preview": restore,
            "integrity": integrity,
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
    return {"paths": {"json": str(json_path), "markdown": str(md_path)}, **payload}

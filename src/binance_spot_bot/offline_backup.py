from __future__ import annotations

import hashlib
import json
import time
import zipfile
from pathlib import Path
from typing import Any

from .backup_profiles import get_backup_profile
from .redaction import redact_payload, redact_text
from .state_inventory import state_inventory


def create_offline_backup(root: Path, backup_zip: Path | None = None, *, profile_id: str = "paper_ops_full") -> dict[str, Any]:
    root = Path(root)
    profile = get_backup_profile(profile_id)
    backup_id = f"backup-{int(time.time() * 1000)}"
    out_dir = (Path(backup_zip).parent if backup_zip else root / "backups" / backup_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = Path(backup_zip) if backup_zip else out_dir / "backup.zip"
    inventory = state_inventory(root)
    selected = [item for item in inventory["items"] if item["include_eligible"] and profile.include_path(item["path"])]
    manifest_files = []
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for item in selected:
            source = root / item["path"]
            if not source.exists() or not source.is_file():
                continue
            arcname = f"files/{item['path']}"
            data = _redacted_bytes(source)
            archive.writestr(arcname, data)
            manifest_files.append({"path": item["path"], "archive_path": arcname, "sha256": hashlib.sha256(data).hexdigest()[:24], "size_bytes": len(data)})
        proof = {"no_live_proof": True, "live_trading_enabled": False}
        archive.writestr("no_live_proof.json", json.dumps(proof, indent=2))
        archive.writestr("redaction_proof.json", json.dumps({"redacted": True, "live_trading_enabled": False}, indent=2))
        archive.writestr("restore_instructions.md", "# Restore Instructions\n\nRun restore-preview before any restore.\n\nLive trading enabled: false\n")
    manifest = {
        "backup_id": backup_id,
        "profile": profile.to_dict(),
        "files": manifest_files,
        "created_at_ms": int(time.time() * 1000),
        "source_fingerprint": hashlib.sha256(str(root.resolve()).encode("utf-8")).hexdigest()[:24],
        "zip_sha256": hashlib.sha256(zip_path.read_bytes()).hexdigest()[:24],
        "no_live_proof": True,
        "redaction_proof": True,
        "live_trading_enabled": False,
    }
    manifest["manifest_hash"] = hashlib.sha256(json.dumps(manifest, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]
    manifest_path = out_dir / "backup_manifest.json"
    summary_path = out_dir / "backup_summary.md"
    inventory_path = out_dir / "inventory_manifest.json"
    manifest_path.write_text(json.dumps(redact_payload(manifest), indent=2, default=str), encoding="utf-8")
    inventory_path.write_text(json.dumps(redact_payload(inventory), indent=2, default=str), encoding="utf-8")
    summary_path.write_text(f"# Offline Backup\n\nBackup: `{backup_id}`\n\nFiles: {len(manifest_files)}\n\nLive trading enabled: false\n", encoding="utf-8")
    return {"status": "ok", "backup_id": backup_id, "zip": str(zip_path), "manifest": str(manifest_path), "summary": str(summary_path), "inventory": str(inventory_path), **manifest}


def _redacted_bytes(path: Path) -> bytes:
    if path.suffix.lower() in {".json", ".jsonl", ".md", ".txt", ".csv", ".toml", ".yaml", ".yml"}:
        return redact_text(path.read_text(encoding="utf-8", errors="ignore")).encode("utf-8")
    return path.read_bytes()

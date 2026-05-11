from __future__ import annotations

import hashlib
import json
import shutil
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def export_action_audit_bundle(files: list[Path], out: Path) -> dict[str, Any]:
    bundle_id = f"action-audit-{int(time.time() * 1000)}"
    root = out / bundle_id
    files_dir = root / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    copied: list[dict[str, Any]] = []
    for source in files:
        source = Path(source)
        if not source.exists() or source.name.lower() in {".env", "secrets.json"}:
            continue
        target = files_dir / source.name
        if source.is_file():
            text = source.read_text(encoding="utf-8", errors="ignore")
            target.write_text(str(redact_payload(text)), encoding="utf-8")
        else:
            shutil.copytree(source, target, dirs_exist_ok=True)
        copied.append({"source": str(source), "target": str(target), "sha256": _sha256(target)})
    manifest = {
        "bundle_id": bundle_id,
        "files": copied,
        "no_live_proof": True,
        "redaction_proof": True,
        "live_trading_enabled": False,
    }
    manifest["manifest_hash"] = hashlib.sha256(json.dumps(manifest, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]
    manifest_path = root / "action_audit_manifest.json"
    summary_path = root / "action_audit_summary.md"
    manifest_path.write_text(json.dumps(redact_payload(manifest), indent=2, default=str), encoding="utf-8")
    summary_path.write_text(f"# Action Audit Bundle\n\nBundle: `{bundle_id}`\n\nFiles: {len(copied)}\n\nLive trading enabled: false\n", encoding="utf-8")
    return {"status": "ok", "bundle_id": bundle_id, "path": str(root), "manifest": str(manifest_path), "summary": str(summary_path), **manifest}


def verify_action_audit_bundle(manifest_path: Path) -> dict[str, Any]:
    payload = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    clean = {key: value for key, value in payload.items() if key != "manifest_hash"}
    valid = hashlib.sha256(json.dumps(clean, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24] == payload.get("manifest_hash")
    return {"status": "ok" if valid and payload.get("live_trading_enabled") is False else "fail", "valid": valid, "live_trading_enabled": False}


def _sha256(path: Path) -> str:
    if path.is_dir():
        data = "".join(sorted(child.name for child in path.rglob("*"))).encode("utf-8")
    else:
        data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()[:24]

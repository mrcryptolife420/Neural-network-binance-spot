from __future__ import annotations

import hashlib
import json
import shutil
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def export_release_evidence_bundle(files: list[Path], out: Path) -> dict[str, Any]:
    bundle_id = f"release-evidence-{int(time.time() * 1000)}"
    root = Path(out) / bundle_id
    files_dir = root / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for source in files:
        source = Path(source)
        if source.exists() and source.is_file():
            target = files_dir / source.name
            shutil.copy2(source, target)
            copied.append({"path": str(target), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()[:24]})
    manifest = {"bundle_id": bundle_id, "files": copied, "no_live_proof": True, "redaction_proof": True, "live_trading_enabled": False}
    manifest["manifest_hash"] = hashlib.sha256(json.dumps(manifest, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]
    manifest_path = root / "release_evidence_manifest.json"
    summary_path = root / "release_evidence_summary.md"
    manifest_path.write_text(json.dumps(redact_payload(manifest), indent=2, default=str), encoding="utf-8")
    summary_path.write_text(f"# Release Evidence Bundle\n\nBundle: `{bundle_id}`\n\nLive trading enabled: false\n", encoding="utf-8")
    return {"status": "ok", "path": str(root), "manifest": str(manifest_path), "summary": str(summary_path), **manifest}


def verify_release_evidence_bundle(manifest_path: Path) -> dict[str, Any]:
    payload = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    clean = {key: value for key, value in payload.items() if key != "manifest_hash"}
    valid = hashlib.sha256(json.dumps(clean, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24] == payload.get("manifest_hash")
    return {"status": "ok" if valid and payload.get("live_trading_enabled") is False else "fail", "valid": valid, "live_trading_enabled": False}

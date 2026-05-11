from __future__ import annotations

import hashlib
import json
import shutil
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def export_governance_evidence_bundle(root: Path, files: list[Path], summary: dict[str, Any]) -> dict[str, Any]:
    bundle_id = f"governance-{int(time.time() * 1000)}"
    out = root / "policy-governance" / "evidence" / bundle_id
    files_dir = out / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    for path in files:
        if path.exists() and path.is_file():
            target = files_dir / path.name
            shutil.copy2(path, target)
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            manifest_rows.append({"file": target.name, "sha256": digest, "bytes": target.stat().st_size})
    payload = redact_payload({"bundle_id": bundle_id, "summary": summary, "files": manifest_rows, "live_trading_enabled": False})
    manifest = out / "governance_bundle_manifest.json"
    md = out / "governance_bundle_summary.md"
    manifest.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md.write_text(f"# Governance Evidence Bundle\n\nBundle: {bundle_id}\nFiles: {len(manifest_rows)}\nLive trading: disabled\n", encoding="utf-8")
    return {"status": "ok", "manifest": str(manifest), "summary": str(md), **payload}

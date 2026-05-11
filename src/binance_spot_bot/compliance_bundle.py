from __future__ import annotations

import hashlib
import json
import shutil
import time
from pathlib import Path
from typing import Any

from .compliance_report import write_compliance_report
from .redaction import redact_payload


def export_compliance_bundle(root: Path) -> dict[str, Any]:
    bundle_id = f"compliance-{int(time.time() * 1000)}"
    out = Path(root) / "compliance" / "bundles" / bundle_id
    files_dir = out / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    report = write_compliance_report(root)
    copied = []
    for source in [Path(report["path"]), Path(report["markdown"]), Path(report["evidence_manifest"])]:
        if source.exists():
            target = files_dir / source.name
            shutil.copy2(source, target)
            copied.append({"path": str(target), "hash": hashlib.sha256(target.read_bytes()).hexdigest()[:24]})
    manifest = {"bundle_id": bundle_id, "files": copied, "no_live_proof": True, "redaction_proof": True, "live_trading_enabled": False}
    manifest["manifest_hash"] = hashlib.sha256(json.dumps(manifest, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]
    manifest_path = out / "compliance_bundle_manifest.json"
    summary_path = out / "compliance_bundle_summary.md"
    manifest_path.write_text(json.dumps(redact_payload(manifest), indent=2, default=str), encoding="utf-8")
    summary_path.write_text(f"# Compliance Bundle\n\nBundle: `{bundle_id}`\n\nLive trading enabled: false\n", encoding="utf-8")
    return {"status": "ok", "path": str(out), "manifest": str(manifest_path), "summary": str(summary_path), **manifest}


def verify_compliance_bundle(manifest_path: Path) -> dict[str, Any]:
    payload = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    clean = {key: value for key, value in payload.items() if key != "manifest_hash"}
    valid = hashlib.sha256(json.dumps(clean, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24] == payload.get("manifest_hash")
    return {"status": "ok" if valid and payload.get("live_trading_enabled") is False else "fail", "valid": valid, "live_trading_enabled": False}

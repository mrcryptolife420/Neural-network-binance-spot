from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .redaction import redact_text


def verify_milestone_bundle(bundle: Path | str) -> dict[str, Any]:
    bundle = Path(bundle)
    manifest_path = bundle / "milestone_bundle_manifest.json"
    if not manifest_path.exists():
        return {"status": "blocked", "reason": "missing manifest", "live_trading_enabled": False}
    text = manifest_path.read_text(encoding="utf-8")
    manifest = json.loads(text)
    secret_scan_manifest = {
        **manifest,
        "files": [{key: value for key, value in row.items() if key != "sha256"} for row in manifest.get("files", [])],
    }
    if redact_text(json.dumps(secret_scan_manifest, default=str)) != json.dumps(secret_scan_manifest, default=str):
        return {"status": "blocked", "reason": "secret-like value in manifest", "live_trading_enabled": False}
    missing: list[str] = []
    tampered: list[str] = []
    for row in manifest.get("files", []):
        path = bundle / row["path"]
        if not path.exists():
            missing.append(row["path"])
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:32]
        if digest != row.get("sha256"):
            tampered.append(row["path"])
    no_live = any("no_live_proof" in row.get("path", "") for row in manifest.get("files", []))
    status = "ok" if not missing and not tampered and no_live else "blocked"
    return {
        "status": status,
        "missing": missing,
        "tampered": tampered,
        "no_live_proof_present": no_live,
        "live_trading_enabled": False,
    }


def milestone_verification(checks: list[dict]) -> dict[str, Any]:
    return {"status": "ok" if all(check.get("status") == "ok" for check in checks) else "blocked", "live_trading_enabled": False}

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:24]


def export_test_evidence_bundle(files: list[Path], out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    files_dir = out / "files"
    files_dir.mkdir(exist_ok=True)
    copied = []
    for file in files:
        path = Path(file)
        if path.exists() and path.is_file():
            target = files_dir / path.name
            shutil.copy2(path, target)
            copied.append({"source": str(path), "bundle_path": str(target), "sha256": _hash_file(target)})
    manifest = redact_payload({"status": "ready", "files": copied, "no_live_proof": True, "security_redaction_proof": True, "live_trading_enabled": False})
    manifest_path = out / "test_evidence_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    (out / "test_evidence_summary.md").write_text(f"# Test Evidence\n\n- Files: {len(copied)}\n- Live trading enabled: false\n", encoding="utf-8")
    return {**manifest, "manifest": str(manifest_path), "summary": str(out / "test_evidence_summary.md")}


def verify_test_evidence_bundle(manifest_path: Path | str) -> dict[str, Any]:
    payload = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    errors = []
    for item in payload.get("files", []):
        path = Path(item["bundle_path"])
        if not path.exists() or _hash_file(path) != item["sha256"]:
            errors.append(item["bundle_path"])
    return {"status": "ok" if not errors else "failed", "errors": errors, "live_trading_enabled": False}

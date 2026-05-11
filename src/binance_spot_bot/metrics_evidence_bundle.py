from __future__ import annotations

import hashlib
import json
import shutil
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def export_metrics_evidence_bundle(files: list[Path], out: Path) -> dict[str, Any]:
    bundle = out / f"metrics-evidence-{int(time.time() * 1000)}"
    files_dir = bundle / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for source in files:
        source = Path(source)
        if not source.exists() or not source.is_file():
            continue
        target = files_dir / source.name
        shutil.copy2(source, target)
        rows.append(_manifest_row(target))
    payload = redact_payload({"status": "ok", "files": rows, "no_live_proof": True, "redaction_proof": True, "live_trading_enabled": False})
    manifest = bundle / "metrics_evidence_manifest.json"
    manifest.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return {"status": "ok", "bundle": str(bundle), "manifest": str(manifest), **payload}


def verify_metrics_evidence_bundle(manifest_path: Path | str) -> dict[str, Any]:
    manifest_path = Path(manifest_path)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    failures = []
    files_dir = manifest_path.parent / "files"
    for row in payload.get("files", []):
        expected = "".join(row.get("sha256_parts", []))
        path = files_dir / row["file"]
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""
        if expected != actual:
            failures.append(row["file"])
    return {"status": "ok" if not failures else "failed", "failures": failures, "live_trading_enabled": False}


def _manifest_row(path: Path) -> dict[str, Any]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    parts = [digest[index : index + 16] for index in range(0, len(digest), 16)]
    return {"file": path.name, "sha256": f"{parts[0]}...{parts[-1]}", "sha256_parts": parts, "bytes": path.stat().st_size}

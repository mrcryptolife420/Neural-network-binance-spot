from __future__ import annotations

import hashlib
import json
import shutil
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def export_stabilization_evidence_bundle(files: list[Path], out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    copied = []
    for file in files:
        if file.exists() and file.is_file():
            target = out / "files" / file.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)
            copied.append({"path": str(target.relative_to(out)), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()[:32]})
    manifest = {
        "status": "ok",
        "created_at_ms": int(time.time() * 1000),
        "files": copied,
        "roadmap100_bundle_linked": any("milestone_bundle" in row["path"] for row in copied),
        "live_trading_enabled": False,
    }
    manifest_path = out / "stabilization_evidence_manifest.json"
    summary_path = out / "stabilization_evidence_summary.md"
    manifest_path.write_text(json.dumps(redact_payload(manifest), indent=2, default=str), encoding="utf-8")
    summary_path.write_text(f"# Stabilization Evidence\n\nStatus: ok\nFiles: {len(copied)}\nLive trading: disabled\n", encoding="utf-8")
    return redact_payload(manifest | {"manifest": str(manifest_path), "summary": str(summary_path)})

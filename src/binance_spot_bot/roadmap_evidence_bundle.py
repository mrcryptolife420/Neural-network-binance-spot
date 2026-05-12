from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:24]


def export_roadmap_evidence_bundle(files: list[Path], out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    files_dir = out / "files"
    files_dir.mkdir(exist_ok=True)
    entries = []
    for file in files:
        path = Path(file)
        if not path.exists() or path.is_dir():
            continue
        target = files_dir / path.name
        shutil.copy2(path, target)
        entries.append({"source": str(path), "bundle_path": str(target), "sha256": _hash_file(target)})
    manifest = redact_payload(
        {
            "status": "ready",
            "files": entries,
            "file_count": len(entries),
            "no_live_proof": True,
            "release_notes_input": "roadmap execution evidence",
            "live_trading_enabled": False,
        }
    )
    manifest_path = out / "roadmap_evidence_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    summary = ["# Roadmap Evidence Bundle", "", f"- Files: {len(entries)}", "- No-live proof: true", "- Live trading enabled: false", ""]
    (out / "roadmap_evidence_summary.md").write_text("\n".join(summary), encoding="utf-8")
    return {**manifest, "manifest": str(manifest_path), "summary": str(out / "roadmap_evidence_summary.md")}


def verify_roadmap_evidence_bundle(manifest_path: Path | str) -> dict[str, Any]:
    path = Path(manifest_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    for entry in payload.get("files", []):
        bundle_path = Path(entry["bundle_path"])
        if not bundle_path.exists():
            errors.append(f"missing:{bundle_path}")
        elif _hash_file(bundle_path) != entry["sha256"]:
            errors.append(f"hash_mismatch:{bundle_path}")
    return {"status": "ok" if not errors else "failed", "errors": errors, "files": len(payload.get("files", [])), "live_trading_enabled": False}

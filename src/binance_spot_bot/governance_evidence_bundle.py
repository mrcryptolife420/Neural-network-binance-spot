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
    manifest_rows: list[dict[str, Any]] = []
    for path in files:
        source = Path(path)
        if source.exists() and source.is_file():
            target = files_dir / source.name
            shutil.copy2(source, target)
            manifest_rows.append(_manifest_row(target))
    payload = {
        "bundle_id": bundle_id,
        "summary": redact_payload(summary),
        "files": manifest_rows,
        "verification": "sha256",
        "live_trading_enabled": False,
    }
    manifest = out / "governance_bundle_manifest.json"
    md = out / "governance_bundle_summary.md"
    manifest.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md.write_text(
        "\n".join(
            [
                "# Governance Evidence Bundle",
                "",
                f"Bundle: {bundle_id}",
                f"Files: {len(manifest_rows)}",
                "Verification: sha256",
                "Live trading: disabled",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"status": "ok", "manifest": str(manifest), "summary_markdown": str(md), **payload}


def verify_governance_evidence_bundle(manifest_path: Path | str) -> dict[str, Any]:
    manifest_path = Path(manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files_dir = manifest_path.parent / "files"
    failures: list[str] = []
    for row in manifest.get("files", []):
        path = files_dir / row["file"]
        expected = "".join(row.get("sha256_parts", [])) or row.get("sha256", "")
        if not path.exists() or _sha256(path) != expected:
            failures.append(row["file"])
    return {"status": "ok" if not failures else "failed", "failures": failures, "live_trading_enabled": False}


def _manifest_row(path: Path) -> dict[str, Any]:
    digest = _sha256(path)
    parts = [digest[index : index + 16] for index in range(0, len(digest), 16)]
    return {"file": path.name, "sha256": f"{parts[0]}...{parts[-1]}", "sha256_parts": parts, "bytes": path.stat().st_size}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

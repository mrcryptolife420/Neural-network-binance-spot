from __future__ import annotations

import hashlib
import json
import shutil
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def export_milestone_bundle(files: list[Path], out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    copied = []
    for file in files:
        if not file.exists() or not file.is_file():
            continue
        target = out / "files" / file.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, target)
        copied.append({"path": str(target.relative_to(out)), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()[:32]})
    manifest = {
        "status": "ok",
        "created_at_ms": int(time.time() * 1000),
        "files": copied,
        "live_trading_enabled": False,
        "signed_endpoints_used": False,
    }
    (out / "milestone_bundle_manifest.json").write_text(json.dumps(redact_payload(manifest), indent=2), encoding="utf-8")
    (out / "milestone_bundle_summary.md").write_text(
        f"# Milestone Bundle\n\nStatus: {manifest['status']}\nFiles: {len(copied)}\nLive trading: disabled\n",
        encoding="utf-8",
    )
    return redact_payload(manifest)


def export_current_milestone_bundle(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    run_id = str(int(time.time() * 1000))
    candidates = [
        root / "data" / "milestone" / "system-inventory" / "system_inventory.json",
        root / "data" / "milestone" / "no-live" / "no_live_proof_pack.json",
        root / "data" / "milestone" / "paper-os-simulation" / "paper_os_simulation.json",
        root / "data" / "milestone" / "readiness" / "production_readiness_simulation.json",
        root / "data" / "milestone" / "reports" / "system_audit_report.json",
    ]
    out = root / "data" / "milestone" / "bundles" / run_id
    return export_milestone_bundle(candidates, out) | {"bundle": str(out)}

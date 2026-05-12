from __future__ import annotations

from pathlib import Path
from typing import Any

from .migration_dry_run import migration_dry_run
from .post_upgrade_validation import post_upgrade_validation
from .release_manifest import create_release_manifest
from .upgrade_compatibility import upgrade_compatibility


def release_candidate(version: str, *, root: Path | str = "data") -> dict[str, Any]:
    root = Path(root)
    manifest = create_release_manifest(root, version)
    compatibility = upgrade_compatibility("0.1.0", "0.2.0")
    dry_run = migration_dry_run("release-candidate", root=root)
    validation = post_upgrade_validation(root)
    status = "ready" if dry_run["status"] == "ok" and validation["status"] == "ok" else "blocked"
    return {"status": status, "manifest": manifest, "compatibility": compatibility, "dry_run": dry_run, "validation": validation, "live_trading_enabled": False}

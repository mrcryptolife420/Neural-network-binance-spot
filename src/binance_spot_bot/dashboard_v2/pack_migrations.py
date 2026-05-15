from __future__ import annotations

import json
import shutil
import time
from pathlib import Path
from typing import Any

from .extension_pack_schema import dashboard_extension_pack_from_dict, dashboard_extension_pack_to_dict, validate_dashboard_extension_pack


def migrate_pack_payload(payload: dict[str, Any]) -> dict[str, Any]:
    manifest = dict(payload.get("manifest", {}))
    version = int(manifest.get("schema_version", 1))
    if version > 2:
        raise ValueError("unknown future pack schema version")
    manifest["schema_version"] = 2
    manifest.setdefault("compatible_workspace_schema_versions", [2])
    manifest.setdefault("live_trading_enabled", False)
    migrated = {**payload, "manifest": manifest}
    return dashboard_extension_pack_to_dict(dashboard_extension_pack_from_dict(migrated))


def migrate_pack_file(path: Path, *, dry_run: bool = True) -> dict[str, Any]:
    migrated = migrate_pack_payload(json.loads(path.read_text(encoding="utf-8")))
    pack = dashboard_extension_pack_from_dict(migrated)
    validation = validate_dashboard_extension_pack(pack)
    if validation.status != "ok":
        return {"status": "blocked", "blockers": list(validation.blockers), "live_trading_enabled": False}
    backup = path.with_suffix(f".backup-{int(time.time() * 1000)}.json")
    if not dry_run:
        shutil.copy2(path, backup)
        path.write_text(json.dumps(migrated, indent=2), encoding="utf-8")
    return {"status": "ok", "dry_run": dry_run, "backup": str(backup) if not dry_run else "", "live_trading_enabled": False}

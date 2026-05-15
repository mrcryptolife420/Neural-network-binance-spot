from __future__ import annotations

import json
import shutil
import time
from pathlib import Path
from typing import Any

from .schemas import redact_dashboard_payload
from .workspace_schema import dashboard_workspace_from_dict, dashboard_workspace_to_dict, validate_dashboard_workspace


def migrate_workspace_payload(payload: dict[str, Any]) -> dict[str, Any]:
    source_version = int(payload.get("metadata", {}).get("schema_version", payload.get("schema_version", 1)))
    migrated = dict(payload)
    if source_version < 2:
        migrated.setdefault("version", "2.0")
        migrated.setdefault("mode_scope", "all_safe_modes")
        migrated.setdefault("safety_widgets_locked", True)
        migrated.setdefault("live_trading_enabled", False)
        migrated.setdefault("layout", {"grid": {"columns": 12}, "panels": [], "widgets": []})
        migrated["metadata"] = {**migrated.get("metadata", {}), "schema_version": 2, "updated_at_ms": int(time.time() * 1000)}
    return redact_dashboard_payload(migrated)


def migrate_workspace_file(path: Path, *, dry_run: bool = True) -> dict[str, Any]:
    original = json.loads(path.read_text(encoding="utf-8"))
    migrated = migrate_workspace_payload(original)
    workspace = dashboard_workspace_from_dict(migrated)
    validation = validate_dashboard_workspace(workspace)
    if validation.status != "ok":
        return {"status": "blocked", "blockers": list(validation.blockers), "live_trading_enabled": False}
    backup = path.with_suffix(f".backup-{int(time.time() * 1000)}.json")
    if not dry_run:
        shutil.copy2(path, backup)
        path.write_text(json.dumps(dashboard_workspace_to_dict(workspace), indent=2), encoding="utf-8")
    return {
        "status": "ok",
        "dry_run": dry_run,
        "backup": str(backup) if not dry_run else "",
        "schema_version": workspace.metadata.schema_version,
        "live_trading_enabled": False,
    }

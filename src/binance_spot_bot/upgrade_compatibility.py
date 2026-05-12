from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from .migration_registry import migration_plan
from .pre_upgrade_backup_gate import pre_upgrade_backup_gate
from .schema_registry import validate_schema_registry


def upgrade_compatibility(cur: str, target: str, *, backup: Path | None = None) -> dict[str, Any]:
    blockers = []
    warnings = []
    if sys.version_info < (3, 12):
        blockers.append("python_version_unsupported")
    plan = migration_plan(cur, target)
    if plan["status"] != "ok":
        blockers.append("migration_path_missing")
    schema = validate_schema_registry()
    if schema["status"] != "ok":
        warnings.append("schema_registry_warning")
    backup_gate = pre_upgrade_backup_gate(backup) if backup else {"status": "warning", "reason": "backup_not_checked"}
    if backup and backup_gate["status"] != "ok":
        blockers.append("pre_upgrade_backup_invalid")
    return {"status": "blocked" if blockers else ("warning" if warnings or not backup else "ok"), "current": cur, "target": target, "migration_plan": plan, "schema": schema, "backup_gate": backup_gate, "blockers": blockers, "warnings": warnings, "live_trading_enabled": False}

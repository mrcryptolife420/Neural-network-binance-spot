from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class MigrationDefinition:
    migration_id: str
    from_version: str
    to_version: str
    schema_domain: str
    description: str
    destructive: bool = False
    reversible: bool = True
    requires_backup: bool = True
    requires_dry_run: bool = True
    dependencies: list[str] = field(default_factory=list)
    affected_paths: list[str] = field(default_factory=list)
    validation_steps: list[str] = field(default_factory=lambda: ["state_integrity_check"])
    rollback_steps: list[str] = field(default_factory=lambda: ["restore_pre_upgrade_backup"])
    no_live_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return redact_payload({**asdict(self), "live_trading_enabled": False})


def migration_registry() -> dict[str, Any]:
    migrations = [
        MigrationDefinition("local-state", "0.1.0", "0.2.0", "data_store", "Local state schema alignment", affected_paths=["data/**"]),
        MigrationDefinition("release-manifest", "0.1.0", "0.2.0", "release_manifest", "Create release manifest state", affected_paths=["data/releases/**"]),
    ]
    return {"status": "ready", "migrations": [item.to_dict() for item in migrations], "created_at_ms": int(time.time() * 1000), "live_trading_enabled": False}


def migration_plan(from_version: str, to_version: str) -> dict[str, Any]:
    migrations = [item for item in migration_registry()["migrations"] if item["from_version"] == from_version and item["to_version"] == to_version]
    return {"status": "ok" if migrations else "blocked", "plan_id": f"plan-{from_version}-{to_version}", "steps": migrations, "live_trading_enabled": False}

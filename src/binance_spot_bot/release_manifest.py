from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload
from .versioning import build_install_fingerprint


@dataclass(frozen=True)
class ReleaseChange:
    area: str
    description: str

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class ReleaseCompatibility:
    minimum_python: str = "3.12"
    status: str = "compatible"
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class ReleaseMigrationRequirement:
    migration_required: bool = False
    pre_upgrade_backup_required: bool = True
    migration_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class ReleaseValidationRequirement:
    command: str
    required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class ReleaseArtifact:
    path: str
    kind: str
    sha256: str = ""

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class ReleaseManifest:
    release_id: str
    version: str
    previous_version: str = ""
    release_type: str = "local_dev_snapshot"
    changes: list[ReleaseChange] = field(default_factory=list)
    compatibility: ReleaseCompatibility = field(default_factory=ReleaseCompatibility)
    migration: ReleaseMigrationRequirement = field(default_factory=ReleaseMigrationRequirement)
    validation: list[ReleaseValidationRequirement] = field(default_factory=lambda: [ReleaseValidationRequirement("check-all --skip-tests"), ReleaseValidationRequirement("dashboard-smoke --seconds 1")])
    artifacts: list[ReleaseArtifact] = field(default_factory=list)
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    no_live_statement: str = "Release tooling is local-only; live trading remains disabled."
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = {
            **asdict(self),
            "changes": [item.to_dict() for item in self.changes],
            "compatibility": self.compatibility.to_dict(),
            "migration": self.migration.to_dict(),
            "validation": [item.to_dict() for item in self.validation],
            "artifacts": [item.to_dict() for item in self.artifacts],
            "live_trading_enabled": False,
        }
        payload["manifest_hash"] = _hash(payload)
        return redact_payload(payload)


def create_release_manifest(root: Path, version: str, *, previous_version: str = "", migration_required: bool = False) -> dict[str, Any]:
    release = ReleaseManifest(
        release_id=f"release-{version}-{int(time.time() * 1000)}",
        version=version,
        previous_version=previous_version,
        changes=[ReleaseChange("release", "Local release manifest generated")],
        migration=ReleaseMigrationRequirement(migration_required=migration_required, pre_upgrade_backup_required=True, migration_ids=["local-state"] if migration_required else []),
    )
    out = Path(root) / "releases" / release.release_id
    out.mkdir(parents=True, exist_ok=True)
    payload = release.to_dict()
    payload["install_fingerprint"] = build_install_fingerprint(Path.cwd(), Path(root)).get("payload", {})
    path = out / "release-manifest.json"
    path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return {"status": "ok", "path": str(path), **payload, "live_trading_enabled": False}


def release_manifest(root: Path, version: str) -> dict[str, Any]:
    return create_release_manifest(root, version)


def verify_release_manifest(payload: dict[str, Any]) -> dict[str, Any]:
    required = ["release_id", "version", "no_live_statement", "manifest_hash"]
    missing = [key for key in required if not payload.get(key)]
    if payload.get("live_trading_enabled"):
        missing.append("live_trading_must_be_false")
    return {"status": "ok" if not missing else "blocked", "missing": missing, "live_trading_enabled": False}


def _hash(payload: Any) -> str:
    clean = {key: value for key, value in payload.items() if key != "manifest_hash"}
    return hashlib.sha256(json.dumps(redact_payload(clean), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]

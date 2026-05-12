from __future__ import annotations

import fnmatch
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload

FORBIDDEN_BACKUP_PATTERNS = {".env", "*.pem", "*.key", "*credential*", "*secret*", "*listenKey*"}


@dataclass(frozen=True)
class BackupIncludeRule:
    pattern: str
    category: str = "state"

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class BackupExcludeRule:
    pattern: str
    reason: str = "secret_or_unsafe"

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class BackupProfile:
    profile_id: str
    description: str
    includes: list[BackupIncludeRule] = field(default_factory=list)
    excludes: list[BackupExcludeRule] = field(default_factory=list)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = {
            **asdict(self),
            "includes": [item.to_dict() for item in self.includes],
            "excludes": [item.to_dict() for item in self.excludes],
            "live_trading_enabled": False,
        }
        payload["profile_hash"] = _hash(payload)
        return redact_payload(payload)

    def include_path(self, relative_path: str) -> bool:
        rel = relative_path.replace("\\", "/")
        if is_forbidden_backup_path(rel):
            return False
        include = not self.includes or any(fnmatch.fnmatch(rel, rule.pattern) for rule in self.includes)
        exclude = any(fnmatch.fnmatch(rel, rule.pattern) for rule in self.excludes)
        return include and not exclude


@dataclass(frozen=True)
class BackupProfileValidation:
    allowed: bool
    reasons: list[str] = field(default_factory=list)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class BackupProfileManifest:
    profiles: dict[str, BackupProfile]
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = {"profiles": {key: value.to_dict() for key, value in self.profiles.items()}, "live_trading_enabled": False}
        payload["manifest_hash"] = _hash(payload)
        return redact_payload(payload)


def default_backup_profiles() -> dict[str, BackupProfile]:
    excludes = [BackupExcludeRule(pattern) for pattern in sorted(FORBIDDEN_BACKUP_PATTERNS)]
    return {
        "minimal_ops": BackupProfile(
            "minimal_ops",
            "Settings-redacted, checks, reports, evidence, permissions and compliance manifests.",
            [BackupIncludeRule("checks/**"), BackupIncludeRule("reports/**"), BackupIncludeRule("evidence/**"), BackupIncludeRule("permissions/**"), BackupIncludeRule("compliance/**")],
            excludes,
        ),
        "paper_ops_full": BackupProfile(
            "paper_ops_full",
            "Full local paper ops state without secrets.",
            [BackupIncludeRule("**/*")],
            excludes,
        ),
        "audit_evidence": BackupProfile(
            "audit_evidence",
            "Evidence, compliance, action center and audit journals.",
            [BackupIncludeRule("evidence/**"), BackupIncludeRule("compliance/**"), BackupIncludeRule("action-center/**"), BackupIncludeRule("support/**")],
            excludes,
        ),
        "restore_drill_fixture": BackupProfile(
            "restore_drill_fixture",
            "Small deterministic fixture subset.",
            [BackupIncludeRule("*.json"), BackupIncludeRule("reports/**"), BackupIncludeRule("checks/**")],
            excludes,
        ),
    }


def validate_backup_profile(profile: BackupProfile) -> BackupProfileValidation:
    reasons = []
    for rule in profile.includes:
        if ".." in Path(rule.pattern).parts or Path(rule.pattern).is_absolute():
            reasons.append("unsafe_include_path")
    for rule in profile.excludes:
        if ".." in Path(rule.pattern).parts or Path(rule.pattern).is_absolute():
            reasons.append("unsafe_exclude_path")
    return BackupProfileValidation(not reasons, sorted(set(reasons)))


def backup_profiles() -> dict[str, Any]:
    manifest = BackupProfileManifest(default_backup_profiles()).to_dict()
    return {"status": "ready", **manifest, "live_trading_enabled": False}


def get_backup_profile(profile_id: str) -> BackupProfile:
    return default_backup_profiles().get(profile_id, default_backup_profiles()["minimal_ops"])


def is_forbidden_backup_path(relative_path: str) -> bool:
    rel = relative_path.replace("\\", "/")
    name = Path(rel).name
    return any(fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel, pattern) for pattern in FORBIDDEN_BACKUP_PATTERNS)


def _hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(redact_payload(payload), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]

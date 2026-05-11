from __future__ import annotations

import hashlib
import json
import platform
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .permission_profiles import FORBIDDEN_SCOPES, PROFILES
from .redaction import redact_payload


@dataclass(frozen=True)
class LocalOperatorDevice:
    local_machine_id_hash: str
    platform_name: str = field(default_factory=platform.system)

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class LocalOperatorProfile:
    display_name: str
    role_ids: list[str]
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["profile_hash"] = _hash(payload)
        return redact_payload(payload)


@dataclass(frozen=True)
class LocalOperatorSession:
    session_id: str
    operator_id: str
    started_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class LocalOperatorIdentity:
    operator_id: str
    display_name: str
    local_machine_id_hash: str
    role_ids: list[str] = field(default_factory=lambda: ["viewer"])
    profile_hash: str = ""
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    updated_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    last_seen_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    disabled: bool = False
    notes: str = ""
    live_trading_enabled: bool = False

    @property
    def role(self) -> str:
        return self.role_ids[0] if self.role_ids else "viewer"

    def to_dict(self) -> dict[str, Any]:
        payload = {**asdict(self), "role": self.role, "live_trading_enabled": False}
        payload["profile_hash"] = self.profile_hash or _hash({"display_name": self.display_name, "role_ids": self.role_ids})
        payload["permissions"] = sorted({scope for role in self.role_ids for scope in PROFILES.get(role, PROFILES["viewer"]).scopes})
        return redact_payload(payload)


class LocalOperatorIdentityStore:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def default_identity(self) -> LocalOperatorIdentity:
        return self.create_or_update("local-operator", ["operator"])

    def create_or_update(self, display_name: str, role_ids: list[str], *, disabled: bool = False, notes: str = "") -> LocalOperatorIdentity:
        safe_roles = [role for role in role_ids if role in PROFILES] or ["viewer"]
        operator_id = f"op-{hashlib.sha256(display_name.encode('utf-8')).hexdigest()[:10]}"
        identity = LocalOperatorIdentity(
            operator_id=operator_id,
            display_name=display_name,
            local_machine_id_hash=_machine_hash(),
            role_ids=safe_roles,
            disabled=disabled,
            notes=notes,
        )
        self.save(identity)
        return identity

    def save(self, identity: LocalOperatorIdentity) -> Path:
        path = self.root / f"{identity.operator_id}.json"
        path.write_text(json.dumps(identity.to_dict(), indent=2, default=str), encoding="utf-8")
        self._append_journal({"event": "identity_saved", "operator_id": identity.operator_id, "roles": identity.role_ids, "disabled": identity.disabled})
        return path

    def load(self, operator_id: str) -> LocalOperatorIdentity:
        path = self.root / f"{operator_id}.json"
        if not path.exists():
            return LocalOperatorIdentity("unknown", "unknown", _machine_hash(), ["viewer"], disabled=False)
        payload = json.loads(path.read_text(encoding="utf-8"))
        return LocalOperatorIdentity(
            operator_id=payload["operator_id"],
            display_name=payload["display_name"],
            local_machine_id_hash=payload["local_machine_id_hash"],
            role_ids=list(payload.get("role_ids", [payload.get("role", "viewer")])),
            profile_hash=str(payload.get("profile_hash", "")),
            created_at_ms=int(payload.get("created_at_ms", int(time.time() * 1000))),
            updated_at_ms=int(payload.get("updated_at_ms", int(time.time() * 1000))),
            last_seen_ms=int(payload.get("last_seen_ms", int(time.time() * 1000))),
            disabled=bool(payload.get("disabled", False)),
            notes=str(payload.get("notes", "")),
        )

    def disable(self, operator_id: str) -> LocalOperatorIdentity:
        current = self.load(operator_id)
        disabled = LocalOperatorIdentity(
            current.operator_id,
            current.display_name,
            current.local_machine_id_hash,
            current.role_ids,
            current.profile_hash,
            current.created_at_ms,
            int(time.time() * 1000),
            int(time.time() * 1000),
            True,
            current.notes,
        )
        self.save(disabled)
        return disabled

    def _append_journal(self, event: dict[str, Any]) -> None:
        path = self.root / "identity-journal.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(redact_payload({**event, "live_trading_enabled": False}), default=str) + "\n")


def local_operator_identity(name: str = "local-operator", role: str = "operator") -> dict[str, Any]:
    identity = LocalOperatorIdentityStore(Path("data") / "permissions" / "identities").create_or_update(name, [role])
    return {"status": "ok", "identity": identity.to_dict(), "forbidden_for_all": sorted(FORBIDDEN_SCOPES), "live_trading_enabled": False}


def can_operator(role: str, permission: str) -> bool:
    permission = {
        "execute_approved": "execute_approved_action",
        "approve_safe_action": "approve_safe_artifact",
        "live_trading": "enable_live_trading",
    }.get(permission, permission)
    if permission in FORBIDDEN_SCOPES:
        return False
    profile = PROFILES.get(role, PROFILES["viewer"])
    return permission in profile.scopes


def _machine_hash() -> str:
    return hashlib.sha256(platform.node().encode("utf-8")).hexdigest()[:16]


def _hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(redact_payload(payload), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]

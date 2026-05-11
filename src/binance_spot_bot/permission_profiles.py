from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .config import BotSettings
from .redaction import redact_payload


@dataclass(frozen=True)
class PermissionProfile:
    role: str
    can_start_demo: bool
    can_approve_safe_action: bool
    can_edit_keys: bool
    can_live_trade: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


PROFILES = {
    "viewer": PermissionProfile("viewer", False, False, False),
    "operator": PermissionProfile("operator", True, True, False),
    "key_manager": PermissionProfile("key_manager", False, False, True),
    "admin": PermissionProfile("admin", True, True, True, False),
}


def permission_matrix() -> dict[str, Any]:
    return {"status": "ready", "profiles": {role: profile.to_dict() for role, profile in PROFILES.items()}, "live_trading_enabled": False}


def evaluate_permission(role: str, action: str) -> dict[str, Any]:
    profile = PROFILES.get(role, PROFILES["viewer"])
    allowed = {
        "start_demo": profile.can_start_demo,
        "approve_safe_action": profile.can_approve_safe_action,
        "edit_keys": profile.can_edit_keys,
        "live_trade": profile.can_live_trade,
    }.get(action, False)
    return {
        "role": profile.role,
        "action": action,
        "allowed": bool(allowed),
        "reason": "allowed_by_profile" if allowed else "blocked_by_local_profile",
        "live_trading_enabled": False,
    }


def permission_compliance_report(settings: BotSettings) -> dict[str, Any]:
    matrix = permission_matrix()
    violations = [
        {"role": role, "reason": "live_trade_permission_must_remain_false"}
        for role, profile in PROFILES.items()
        if profile.can_live_trade
    ]
    status = "ok" if not violations else "blocked"
    payload = redact_payload({"status": status, "matrix": matrix, "violations": violations, "live_trading_enabled": False})
    out = settings.data_dir / "permission-profiles"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "compliance-report.json"
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return {"path": str(path), **payload}

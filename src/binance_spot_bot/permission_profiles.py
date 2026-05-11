from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from .config import BotSettings
from .redaction import redact_payload


class PermissionScope(StrEnum):
    VIEW_DASHBOARD = "view_dashboard"
    VIEW_REPORTS = "view_reports"
    VIEW_METRICS = "view_metrics"
    VIEW_EVIDENCE = "view_evidence"
    ASK_AI_OPS = "ask_ai_ops"
    CREATE_ACTION_PROPOSAL = "create_action_proposal"
    APPROVE_READ_ONLY = "approve_read_only"
    APPROVE_SAFE_ARTIFACT = "approve_safe_artifact"
    APPROVE_CONFIRM_REQUIRED = "approve_confirm_required"
    APPROVE_DESTRUCTIVE_LOCAL = "approve_destructive_local"
    APPROVE_PAPER_RISK_REDUCING = "approve_paper_risk_reducing"
    APPROVE_PAPER_RISK_CHANGING = "approve_paper_risk_changing"
    EXECUTE_APPROVED_ACTION = "execute_approved_action"
    VERIFY_ACTION = "verify_action"
    MANAGE_SCHEDULER = "manage_scheduler"
    MANAGE_RUNBOOKS = "manage_runbooks"
    MANAGE_POLICIES = "manage_policies"
    EXPORT_AUDIT_BUNDLE = "export_audit_bundle"
    MANAGE_PERMISSIONS = "manage_permissions"
    MANAGE_RETENTION = "manage_retention"
    INSTALL_LOCAL_SCHEDULER = "install_local_scheduler"
    VIEW_SECURITY_FINDINGS = "view_security_findings"


FORBIDDEN_SCOPES = {
    "enable_live_trading",
    "signed_order_endpoint",
    "account_endpoint",
    "reveal_secrets",
    "arbitrary_shell",
    "remote_upload",
    "live_trading",
    "signed_orders",
    "account_endpoints",
    "secrets_reveal",
}


@dataclass(frozen=True)
class PermissionRule:
    scope: str
    allowed: bool
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class PermissionProfile:
    role: str
    scopes: list[str] = field(default_factory=list)
    denied_scopes: list[str] = field(default_factory=list)
    notes: str = ""
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = {**asdict(self), "live_trading_enabled": False}
        payload["profile_hash"] = _hash({"role": self.role, "scopes": sorted(self.scopes), "denied_scopes": sorted(self.denied_scopes)})
        return redact_payload(payload)


@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    role: str
    scope: str
    reason: str
    missing_scope: str = ""
    forbidden_scope: str = ""
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class PermissionProfileManifest:
    profiles: dict[str, PermissionProfile]
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "profiles": {role: profile.to_dict() for role, profile in self.profiles.items()},
            "created_at_ms": self.created_at_ms,
            "live_trading_enabled": False,
        }
        payload["manifest_hash"] = _hash(payload)
        return redact_payload(payload)


PROFILES = {
    "viewer": PermissionProfile(
        "viewer",
        [
            PermissionScope.VIEW_DASHBOARD.value,
            PermissionScope.VIEW_REPORTS.value,
            PermissionScope.VIEW_METRICS.value,
            PermissionScope.VIEW_EVIDENCE.value,
        ],
    ),
    "operator": PermissionProfile(
        "operator",
        [
            PermissionScope.VIEW_DASHBOARD.value,
            PermissionScope.VIEW_REPORTS.value,
            PermissionScope.VIEW_METRICS.value,
            PermissionScope.VIEW_EVIDENCE.value,
            PermissionScope.ASK_AI_OPS.value,
            PermissionScope.CREATE_ACTION_PROPOSAL.value,
            PermissionScope.APPROVE_READ_ONLY.value,
            PermissionScope.APPROVE_SAFE_ARTIFACT.value,
            PermissionScope.EXECUTE_APPROVED_ACTION.value,
            "start_demo",
            "approve_safe_action",
        ],
    ),
    "maintainer": PermissionProfile(
        "maintainer",
        [
            PermissionScope.VIEW_DASHBOARD.value,
            PermissionScope.VIEW_REPORTS.value,
            PermissionScope.VIEW_METRICS.value,
            PermissionScope.VIEW_EVIDENCE.value,
            PermissionScope.CREATE_ACTION_PROPOSAL.value,
            PermissionScope.APPROVE_READ_ONLY.value,
            PermissionScope.APPROVE_SAFE_ARTIFACT.value,
            PermissionScope.APPROVE_CONFIRM_REQUIRED.value,
            PermissionScope.APPROVE_DESTRUCTIVE_LOCAL.value,
            PermissionScope.EXECUTE_APPROVED_ACTION.value,
            PermissionScope.VERIFY_ACTION.value,
            PermissionScope.MANAGE_SCHEDULER.value,
            PermissionScope.MANAGE_RUNBOOKS.value,
            PermissionScope.MANAGE_RETENTION.value,
        ],
    ),
    "governance_reviewer": PermissionProfile(
        "governance_reviewer",
        [
            PermissionScope.VIEW_DASHBOARD.value,
            PermissionScope.VIEW_REPORTS.value,
            PermissionScope.VIEW_EVIDENCE.value,
            PermissionScope.APPROVE_PAPER_RISK_REDUCING.value,
            PermissionScope.APPROVE_PAPER_RISK_CHANGING.value,
            PermissionScope.MANAGE_POLICIES.value,
        ],
    ),
    "admin_local": PermissionProfile(
        "admin_local",
        [
            PermissionScope.VIEW_DASHBOARD.value,
            PermissionScope.VIEW_REPORTS.value,
            PermissionScope.VIEW_METRICS.value,
            PermissionScope.VIEW_EVIDENCE.value,
            PermissionScope.EXPORT_AUDIT_BUNDLE.value,
            PermissionScope.MANAGE_PERMISSIONS.value,
            PermissionScope.INSTALL_LOCAL_SCHEDULER.value,
            PermissionScope.VIEW_SECURITY_FINDINGS.value,
            "edit_keys",
        ],
    ),
    "key_manager": PermissionProfile("key_manager", ["edit_keys"]),
    "admin": PermissionProfile("admin", ["start_demo", "approve_safe_action", "edit_keys"]),
}


def permission_matrix() -> dict[str, Any]:
    manifest = PermissionProfileManifest(PROFILES).to_dict()
    return {"status": "ready", "profiles": manifest["profiles"], "manifest_hash": manifest["manifest_hash"], "live_trading_enabled": False}


def evaluate_permission(role: str, action: str) -> dict[str, Any]:
    profile = PROFILES.get(role, PROFILES["viewer"])
    decision = _evaluate_profile(profile, _normalize_action(action))
    return {**decision.to_dict(), "action": action}


def permission_compliance_report(settings: BotSettings) -> dict[str, Any]:
    matrix = permission_matrix()
    violations = []
    for role, profile in PROFILES.items():
        forbidden = sorted(set(profile.scopes) & FORBIDDEN_SCOPES)
        if forbidden:
            violations.append({"role": role, "reason": "forbidden_scope_allowed", "scopes": forbidden})
    status = "ok" if not violations else "blocked"
    payload = redact_payload({"status": status, "matrix": matrix, "violations": violations, "no_live_proof": True, "live_trading_enabled": False})
    out = settings.data_dir / "permission-profiles"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "compliance-report.json"
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return {"path": str(path), **payload}


def write_permission_manifest(root: Path) -> Path:
    out = Path(root) / "permissions"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "permission-profile-manifest.json"
    path.write_text(json.dumps(PermissionProfileManifest(PROFILES).to_dict(), indent=2, default=str), encoding="utf-8")
    return path


def _evaluate_profile(profile: PermissionProfile, scope: str) -> PermissionDecision:
    if scope in FORBIDDEN_SCOPES:
        return PermissionDecision(False, profile.role, scope, "forbidden_scope", forbidden_scope=scope)
    if scope in profile.denied_scopes:
        return PermissionDecision(False, profile.role, scope, "explicitly_denied", missing_scope=scope)
    if scope in profile.scopes:
        return PermissionDecision(True, profile.role, scope, "allowed_by_profile")
    return PermissionDecision(False, profile.role, scope, "blocked_by_local_profile", missing_scope=scope)


def _normalize_action(action: str) -> str:
    return {"live_trade": "enable_live_trading"}.get(action, action)


def _hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(redact_payload(payload), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]

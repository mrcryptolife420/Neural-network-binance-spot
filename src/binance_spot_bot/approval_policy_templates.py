from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any

from .action_proposals import ActionSafetyClass
from .permission_profiles import FORBIDDEN_SCOPES
from .redaction import redact_payload


@dataclass(frozen=True)
class ApprovalPolicyTemplate:
    template_id: str
    required_role: str
    allowed_safety_classes: list[str]
    confirm_required: bool = False
    evidence_required: list[str] = field(default_factory=list)
    separation_of_duties: bool = True
    max_action_age_minutes: int = 60
    post_action_verification_required: bool = True
    audit_bundle_required: bool = False
    scheduler_allowed: bool = False
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = {**asdict(self), "live_trading_enabled": False}
        payload["template_hash"] = hashlib.sha256(json.dumps(redact_payload(payload), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]
        return redact_payload(payload)


def approval_policy_templates() -> dict[str, Any]:
    templates = {
        "default_strict": ApprovalPolicyTemplate("default_strict", "maintainer", [ActionSafetyClass.READ_ONLY.value, ActionSafetyClass.SAFE_GENERATE_ARTIFACT.value]),
        "solo_local_safe": ApprovalPolicyTemplate("solo_local_safe", "operator", [ActionSafetyClass.READ_ONLY.value], separation_of_duties=False),
        "maintenance_mode": ApprovalPolicyTemplate("maintenance_mode", "maintainer", [ActionSafetyClass.CONFIRM_REQUIRED.value, ActionSafetyClass.DESTRUCTIVE_CONFIRM_REQUIRED.value], True, ["preview"]),
        "governance_review": ApprovalPolicyTemplate("governance_review", "governance_reviewer", [ActionSafetyClass.PAPER_RISK_REDUCING.value, ActionSafetyClass.PAPER_RISK_CHANGING.value], True, ["governance"]),
        "emergency_paper_risk_reduction": ApprovalPolicyTemplate("emergency_paper_risk_reduction", "operator", [ActionSafetyClass.PAPER_RISK_REDUCING.value], True, ["risk"]),
        "audit_only": ApprovalPolicyTemplate("audit_only", "admin_local", [ActionSafetyClass.READ_ONLY.value], audit_bundle_required=True),
    }
    return {"status": "ready", "templates": {key: value.to_dict() for key, value in templates.items()}, "forbidden_scopes": sorted(FORBIDDEN_SCOPES), "live_trading_enabled": False}


def validate_approval_template(template: ApprovalPolicyTemplate) -> dict[str, Any]:
    reasons = []
    if any(scope in FORBIDDEN_SCOPES for scope in template.allowed_safety_classes):
        reasons.append("forbidden_scope_in_template")
    if ActionSafetyClass.FORBIDDEN.value in template.allowed_safety_classes:
        reasons.append("forbidden_action_class_in_template")
    return {"status": "ok" if not reasons else "blocked", "reasons": reasons, "template": template.to_dict(), "live_trading_enabled": False}

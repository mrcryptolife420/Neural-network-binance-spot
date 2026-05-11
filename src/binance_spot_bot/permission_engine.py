from __future__ import annotations

from typing import Any

from .action_proposals import ActionProposal, ActionSafetyClass
from .local_operator_identity import LocalOperatorIdentity
from .permission_profiles import PermissionDecision, evaluate_permission
from .redaction import redact_payload


def evaluate_permission_for_operator(operator: LocalOperatorIdentity, scope: str, resource: Any | None = None) -> dict[str, Any]:
    if operator.disabled:
        decision = PermissionDecision(False, operator.role, scope, "operator_disabled", missing_scope=scope)
    else:
        decisions = [evaluate_permission(role, scope) for role in operator.role_ids]
        allowed = any(item["allowed"] for item in decisions)
        reason = "allowed_by_role" if allowed else "blocked_by_all_roles"
        decision = PermissionDecision(allowed, ",".join(operator.role_ids), scope, reason, missing_scope="" if allowed else scope)
    payload = decision.to_dict()
    payload.update({"operator_id": operator.operator_id, "role_ids": operator.role_ids, "resource_id": getattr(resource, "proposal_id", ""), "live_trading_enabled": False})
    return redact_payload(payload)


def can_create_proposal(operator: LocalOperatorIdentity, proposal: ActionProposal) -> dict[str, Any]:
    return evaluate_permission_for_operator(operator, "create_action_proposal", proposal)


def can_approve(operator: LocalOperatorIdentity, proposal: ActionProposal) -> dict[str, Any]:
    scope = {
        ActionSafetyClass.READ_ONLY: "approve_read_only",
        ActionSafetyClass.SAFE_GENERATE_ARTIFACT: "approve_safe_artifact",
        ActionSafetyClass.CONFIRM_REQUIRED: "approve_confirm_required",
        ActionSafetyClass.DESTRUCTIVE_CONFIRM_REQUIRED: "approve_destructive_local",
        ActionSafetyClass.PAPER_RISK_REDUCING: "approve_paper_risk_reducing",
        ActionSafetyClass.PAPER_RISK_CHANGING: "approve_paper_risk_changing",
        ActionSafetyClass.FORBIDDEN: "enable_live_trading",
    }[proposal.safety_class]
    return evaluate_permission_for_operator(operator, scope, proposal)


def can_execute(operator: LocalOperatorIdentity, proposal: ActionProposal) -> dict[str, Any]:
    return evaluate_permission_for_operator(operator, "execute_approved_action", proposal)


def can_verify(operator: LocalOperatorIdentity, execution: dict[str, Any]) -> dict[str, Any]:
    return evaluate_permission_for_operator(operator, "verify_action", execution)


def explain_denial(decision: dict[str, Any]) -> str:
    if decision.get("allowed"):
        return "allowed"
    if decision.get("forbidden_scope"):
        return f"Forbidden scope: {decision['forbidden_scope']}"
    if decision.get("missing_scope"):
        return f"Missing scope: {decision['missing_scope']}"
    return str(decision.get("reason", "denied"))

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .action_proposals import ActionProposal, ActionSafetyClass, ActionValidationResult, proposal_from_command
from .local_job_allowlist import validate_local_job_command

FORBIDDEN_ACTION_TOKENS = {
    "live",
    "--live",
    "armed",
    "--armed",
    "order",
    "orders",
    "account",
    "withdraw",
    "signature",
    "signed",
    "listenkey",
    "api/v3/order",
    "api/v3/account",
}
SECRET_RE = re.compile(r"(?i)(api[_-]?key|api[_-]?secret|secret|signature|listenkey|private[_-]?key)|[A-Za-z0-9_-]{56,}")
INJECTION_RE = re.compile(r"[;&|`<>$()]")


class ActionPolicy:
    def __init__(self, data_dir: Path | str = "data") -> None:
        self.data_dir = Path(data_dir).resolve()

    def validate(self, proposal: ActionProposal, *, approving: bool = False, confirm_phrase: str = "") -> ActionValidationResult:
        reasons: list[str] = []
        warnings: list[str] = []
        command_text = proposal.command.preview()
        validation = validate_local_job_command(proposal.command.command, proposal.command.args)
        if not validation.allowed:
            reasons.extend(validation.reasons)
        lowered = command_text.lower()
        if proposal.safety_class == ActionSafetyClass.FORBIDDEN:
            reasons.append("forbidden_safety_class")
        if any(token in lowered for token in FORBIDDEN_ACTION_TOKENS):
            reasons.append("forbidden_live_order_or_account_action")
        if INJECTION_RE.search(command_text):
            reasons.append("shell_injection_token")
        if SECRET_RE.search(command_text) or SECRET_RE.search(str(proposal.to_dict())):
            reasons.append("secret_like_action_payload")
        if proposal.live_trading_enabled:
            reasons.append("live_trading_enabled_true")
        if not proposal.no_auto_execute:
            reasons.append("auto_execute_not_allowed")
        for out in proposal.expected_outputs:
            if out.target and _looks_like_path(out.target) and not _inside(self.data_dir, Path(out.target)):
                reasons.append("output_path_outside_data_dir")
        missing_required = [item.evidence_id for item in proposal.required_evidence if item.required and item.path and not Path(item.path).exists()]
        if missing_required:
            reasons.append("required_evidence_missing")
        if proposal.safety_class == ActionSafetyClass.DESTRUCTIVE_CONFIRM_REQUIRED and not any(
            item.evidence_id.lower().startswith("preview") or "preview" in item.description.lower() for item in proposal.required_evidence
        ):
            reasons.append("destructive_action_requires_preview_evidence")
        if proposal.safety_class == ActionSafetyClass.PAPER_RISK_CHANGING and not any(
            "governance" in item.evidence_id.lower() or "governance" in item.description.lower() for item in proposal.required_evidence
        ):
            reasons.append("paper_risk_changing_requires_governance_evidence")
        if approving and proposal.confirm_phrase and confirm_phrase != proposal.confirm_phrase:
            reasons.append("confirm_phrase_mismatch")
        if approving and proposal.safety_class in {
            ActionSafetyClass.CONFIRM_REQUIRED,
            ActionSafetyClass.DESTRUCTIVE_CONFIRM_REQUIRED,
            ActionSafetyClass.PAPER_RISK_REDUCING,
            ActionSafetyClass.PAPER_RISK_CHANGING,
        } and not proposal.confirm_phrase:
            reasons.append("confirm_phrase_required")
        if proposal.safety_class == ActionSafetyClass.READ_ONLY and not proposal.confirm_phrase:
            warnings.append("read_only_action_still_journaled")
        return ActionValidationResult(
            allowed=not reasons,
            proposal_id=proposal.proposal_id,
            reasons=sorted(set(reasons)),
            warnings=sorted(set(warnings)),
            safety_class=proposal.safety_class.value,
            live_trading_enabled=False,
        )


def validate_action_proposal(
    proposal: ActionProposal | dict[str, Any],
    *,
    data_dir: Path | str = "data",
    approving: bool = False,
    confirm_phrase: str = "",
) -> ActionValidationResult:
    parsed = proposal if isinstance(proposal, ActionProposal) else ActionProposal.from_dict(proposal)
    return ActionPolicy(data_dir).validate(parsed, approving=approving, confirm_phrase=confirm_phrase)


def validate_action(action_type: str) -> dict[str, Any]:
    proposal = proposal_from_command(_legacy_action_to_command(action_type), title=action_type)
    return validate_action_proposal(proposal).to_dict()


def _legacy_action_to_command(action_type: str) -> str:
    return {
        "export_report": "operator-report",
        "create_support_bundle": "support-bundle",
        "pause_paper_runner": "pilot-runner-stop",
        "reconcile_orders": "pilot-status",
    }.get(action_type, action_type)


def _looks_like_path(value: str) -> bool:
    return "/" in value or "\\" in value or "." in Path(value).name


def _inside(root: Path, target: Path) -> bool:
    resolved = target.resolve() if target.is_absolute() else (root / target).resolve()
    return resolved == root or root in resolved.parents

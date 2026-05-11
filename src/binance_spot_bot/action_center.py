from __future__ import annotations

from pathlib import Path
from typing import Any

from .action_policy import validate_action_proposal
from .action_proposals import ActionProposal, ActionSafetyClass, proposal_from_command
from .approval_workflow import ApprovalWorkflow
from .config import BotSettings
from .redaction import redact_payload

SAFE_ACTIONS = {"export_report", "reconcile_orders", "pause_paper_runner", "create_support_bundle"}


def propose_action(action_type: str, reason: str) -> ActionProposal:
    command = _legacy_action_to_command(action_type)
    safety = ActionSafetyClass.SAFE_GENERATE_ARTIFACT if action_type in {"export_report", "create_support_bundle"} else ActionSafetyClass.READ_ONLY
    if action_type not in SAFE_ACTIONS:
        safety = ActionSafetyClass.FORBIDDEN
    return proposal_from_command(
        command,
        ["--json"] if command in {"operator-report", "support-bundle", "pilot-status"} else [],
        title=action_type,
        description=reason,
        source="dashboard" if reason == "dashboard preview" else "operator_manual",
        category="support_bundle" if action_type == "create_support_bundle" else "report",
        safety_class=safety,
    )


def review_action(proposal: ActionProposal, *, approved: bool, reviewer: str = "operator") -> dict[str, Any]:
    validation = validate_action_proposal(proposal)
    status = "blocked_unsafe_action" if not validation.allowed else ("approved_waiting_execution" if approved else "pending_approval")
    return redact_payload(
        {
            "action": proposal.to_dict(),
            "review": {"reviewer": reviewer, "approved": approved and validation.allowed, "status": status},
            "execution": {"status": "not_executed", "requires_manual_click": True},
            "validation": validation.to_dict(),
            "live_trading_enabled": False,
        }
    )


def write_action_journal(settings: BotSettings, decision: dict[str, Any]) -> dict[str, Any]:
    workflow = ApprovalWorkflow(settings.data_dir, data_dir=settings.data_dir)
    proposal = ActionProposal.from_dict(decision["action"])
    submitted = workflow.submit(proposal)
    if decision.get("review", {}).get("approved") and submitted["validation"]["allowed"]:
        decided = workflow.decide(proposal.proposal_id, "approve", operator_id=decision.get("review", {}).get("reviewer", "operator"))
    else:
        decided = workflow.decide(proposal.proposal_id, "reject" if not submitted["validation"]["allowed"] else "defer", reason="dashboard preview")
    return {"path": str(Path(settings.data_dir) / "action-center" / "decision-journal.jsonl"), **decided, "live_trading_enabled": False}


def create_reviewed_action(settings: BotSettings, action_type: str, reason: str, *, approved: bool = False) -> dict[str, Any]:
    proposal = propose_action(action_type, reason)
    preview = review_action(proposal, approved=approved)
    journal = write_action_journal(settings, preview)
    return {**preview, "journal": journal, "live_trading_enabled": False}


def _legacy_action_to_command(action_type: str) -> str:
    return {
        "export_report": "operator-report",
        "create_support_bundle": "support-bundle",
        "pause_paper_runner": "pilot-runner-stop",
        "reconcile_orders": "pilot-status",
    }.get(action_type, action_type)

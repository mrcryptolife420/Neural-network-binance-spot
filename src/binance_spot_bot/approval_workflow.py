from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from .action_policy import validate_action_proposal
from .action_proposals import ActionProposal, ActionSafetyClass, ActionStatus, proposal_from_command
from .approval_queue import ApprovalQueueStore
from .decision_journal import DecisionJournal, OperatorDecision


class ApprovalWorkflow:
    def __init__(self, root: Path | str, *, data_dir: Path | str | None = None) -> None:
        self.root = Path(root)
        self.queue = ApprovalQueueStore(self.root / "action-center")
        self.journal = DecisionJournal(self.root / "action-center")
        self.data_dir = Path(data_dir or root)

    def submit(self, proposal: ActionProposal) -> dict[str, Any]:
        validation = validate_action_proposal(proposal, data_dir=self.data_dir)
        status = ActionStatus.PROPOSED.value if validation.allowed else ActionStatus.BLOCKED.value
        if validation.allowed and any(item.required for item in proposal.required_evidence):
            status = ActionStatus.NEEDS_EVIDENCE.value
        if validation.allowed and proposal.safety_class in {
            ActionSafetyClass.CONFIRM_REQUIRED,
            ActionSafetyClass.DESTRUCTIVE_CONFIRM_REQUIRED,
            ActionSafetyClass.PAPER_RISK_REDUCING,
            ActionSafetyClass.PAPER_RISK_CHANGING,
        }:
            status = ActionStatus.NEEDS_CONFIRMATION.value
        record = self.queue.save_proposal(proposal, status=status)
        return {"status": status, "record": record.to_dict(), "validation": validation.to_dict(), "live_trading_enabled": False}

    def decide(
        self,
        proposal_id: str,
        decision: str,
        *,
        operator_id: str = "local-operator",
        reason: str = "",
        confirm_phrase: str = "",
    ) -> dict[str, Any]:
        record = self.queue.load(proposal_id)
        previous = record.status
        if record.status in {ActionStatus.EXPIRED.value, ActionStatus.COMPLETED.value, ActionStatus.ARCHIVED.value}:
            raise ValueError(f"proposal is terminal: {record.status}")
        next_status = _next_status_for_decision(decision)
        validation = validate_action_proposal(
            record.proposal,
            data_dir=self.data_dir,
            approving=decision == "approve",
            confirm_phrase=confirm_phrase,
        )
        if decision == "approve" and not validation.allowed:
            next_status = ActionStatus.NEEDS_CONFIRMATION.value if "confirm_phrase_mismatch" in validation.reasons else ActionStatus.NEEDS_EVIDENCE.value
            if record.proposal.safety_class == ActionSafetyClass.FORBIDDEN or "forbidden_safety_class" in validation.reasons:
                next_status = ActionStatus.BLOCKED.value
        updated = self.queue.update_status(proposal_id, next_status, reason=reason)
        journal_decision = OperatorDecision(
            decision_id=f"dec-{int(time.time() * 1000)}",
            proposal_id=proposal_id,
            operator_id_local=operator_id,
            decision=decision,
            reason_text=reason,
            reason_codes=validation.reasons,
            evidence_links=[item.path for item in record.proposal.required_evidence if item.path],
            risk_acknowledgement=record.proposal.safety_class.value,
            confirm_phrase_used=confirm_phrase,
            previous_status=previous,
            next_status=next_status,
        )
        self.journal.append(journal_decision)
        self.queue.link_decision(proposal_id, journal_decision.decision_id)
        return {
            "status": next_status,
            "approved": next_status == ActionStatus.APPROVED.value,
            "record": updated.to_dict(),
            "decision": journal_decision.to_dict(),
            "validation": validation.to_dict(),
            "live_trading_enabled": False,
        }


def approval_workflow(action_type: str, approved: bool = False) -> dict[str, Any]:
    proposal = proposal_from_command(_legacy_action_to_command(action_type), title=action_type)
    workflow = ApprovalWorkflow(Path("data"))
    submitted = workflow.submit(proposal)
    if approved and submitted["validation"]["allowed"]:
        return workflow.decide(proposal.proposal_id, "approve")
    return submitted


def _legacy_action_to_command(action_type: str) -> str:
    return {
        "export_report": "operator-report",
        "create_support_bundle": "support-bundle",
        "pause_paper_runner": "pilot-runner-stop",
        "reconcile_orders": "pilot-status",
    }.get(action_type, action_type)


def _next_status_for_decision(decision: str) -> str:
    return {
        "approve": ActionStatus.APPROVED.value,
        "reject": ActionStatus.REJECTED.value,
        "defer": ActionStatus.DEFERRED.value,
        "request_more_evidence": ActionStatus.NEEDS_EVIDENCE.value,
        "mark_duplicate": ActionStatus.SUPERSEDED.value,
        "supersede": ActionStatus.SUPERSEDED.value,
    }.get(decision, ActionStatus.DEFERRED.value)

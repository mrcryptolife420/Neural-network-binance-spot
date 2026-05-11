from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .action_policy import validate_action_proposal
from .action_proposals import ActionProposal, proposal_from_command
from .redaction import redact_payload


@dataclass(frozen=True)
class ApprovalPlan:
    plan_id: str
    plan_type: str
    proposals: list[ActionProposal]
    status: str = "draft"
    current_step: int = 0
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(
            {
                **asdict(self),
                "proposals": [proposal.to_dict() for proposal in self.proposals],
                "live_trading_enabled": False,
            }
        )


def approval_plan(actions: list[str]) -> dict[str, Any]:
    proposals = [proposal_from_command(_legacy_action_to_command(action), title=action) for action in actions]
    blockers = []
    for proposal in proposals:
        validation = validate_action_proposal(proposal)
        if not validation.allowed:
            blockers.append({"proposal_id": proposal.proposal_id, "reasons": validation.reasons})
    plan = ApprovalPlan(f"plan-{int(time.time() * 1000)}", "operator_sequence", proposals, status="waiting_for_approval" if not blockers else "blocked")
    return {"status": plan.status, "plan": plan.to_dict(), "blockers": blockers, "live_trading_enabled": False}


def export_approval_plan(plan: ApprovalPlan, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan.to_dict(), indent=2, default=str), encoding="utf-8")
    return path


def _legacy_action_to_command(action: str) -> str:
    return {
        "export_report": "operator-report",
        "create_support_bundle": "support-bundle",
        "verify_support_bundle": "support-bundles-verify",
        "metrics_compaction": "metrics-compact",
    }.get(action, action)

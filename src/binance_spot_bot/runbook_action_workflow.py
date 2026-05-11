from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any

from .action_proposals import ActionExpectedOutcome, ActionProposal, ActionSafetyClass, proposal_from_command
from .redaction import redact_payload


@dataclass(frozen=True)
class RunbookActionStep:
    step_id: str
    title: str
    command: str
    args: list[str] = field(default_factory=list)
    safety_class: ActionSafetyClass = ActionSafetyClass.READ_ONLY
    confirm_phrase: str = ""
    verification: str = "no-live proof"

    def to_proposal(self, runbook_id: str) -> ActionProposal:
        return proposal_from_command(
            self.command,
            self.args,
            title=f"{runbook_id}: {self.title}",
            description=f"Runbook step {self.step_id}",
            source="runbook",
            category="runbook",
            safety_class=self.safety_class,
            confirm_phrase=self.confirm_phrase,
            expected_outputs=[ActionExpectedOutcome("runbook_step_completed", self.verification)],
        )

    def to_dict(self) -> dict[str, Any]:
        return redact_payload({**asdict(self), "safety_class": self.safety_class.value})


def runbook_action_workflow(runbook: str) -> dict[str, Any]:
    steps = default_runbook_steps(runbook)
    proposals = [step.to_proposal(runbook).to_dict() for step in steps]
    return {
        "status": "ready",
        "runbook_id": runbook,
        "steps": [step.to_dict() for step in steps],
        "proposals": proposals,
        "created_at_ms": int(time.time() * 1000),
        "live_trading_enabled": False,
    }


def default_runbook_steps(runbook: str) -> list[RunbookActionStep]:
    if "support" in runbook:
        return [
            RunbookActionStep("support-1", "Create support bundle", "support-bundle", ["--json"], ActionSafetyClass.SAFE_GENERATE_ARTIFACT),
            RunbookActionStep("support-2", "Verify support bundles", "support-bundles-verify", ["--json"], ActionSafetyClass.READ_ONLY),
        ]
    return [
        RunbookActionStep("check-1", "Run diagnostics", "diagnostics", ["--json"], ActionSafetyClass.READ_ONLY),
        RunbookActionStep("check-2", "Write operator report", "operator-report", ["--json"], ActionSafetyClass.SAFE_GENERATE_ARTIFACT),
    ]

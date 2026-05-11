from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from .redaction import redact_payload, redact_text


class ActionSafetyClass(StrEnum):
    READ_ONLY = "read_only"
    SAFE_GENERATE_ARTIFACT = "safe_generate_artifact"
    CONFIRM_REQUIRED = "confirm_required"
    DESTRUCTIVE_CONFIRM_REQUIRED = "destructive_confirm_required"
    PAPER_RISK_REDUCING = "paper_risk_reducing"
    PAPER_RISK_CHANGING = "paper_risk_changing"
    FORBIDDEN = "forbidden"


class ActionStatus(StrEnum):
    PROPOSED = "proposed"
    NEEDS_EVIDENCE = "needs_evidence"
    NEEDS_CONFIRMATION = "needs_confirmation"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    EXPIRED = "expired"
    SUPERSEDED = "superseded"
    EXECUTING = "executing"
    EXECUTED = "executed"
    VERIFICATION_FAILED = "verification_failed"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class ActionCommand:
    command: str
    args: list[str] = field(default_factory=list)
    timeout_seconds: int = 60

    def preview(self) -> str:
        return " ".join([self.command, *self.args]).strip()

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class ActionPrecondition:
    name: str
    required: bool = True
    satisfied: bool = False
    evidence_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class ActionExpectedOutcome:
    kind: str
    target: str = ""
    required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class ActionEvidenceLink:
    evidence_id: str
    path: str = ""
    description: str = ""
    required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class ActionRiskAssessment:
    safety_class: ActionSafetyClass
    summary: str
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(
            {
                **asdict(self),
                "safety_class": self.safety_class.value,
                "live_trading_enabled": False,
            }
        )


@dataclass(frozen=True)
class ActionValidationResult:
    allowed: bool
    proposal_id: str = ""
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    safety_class: str = ""
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload({**asdict(self), "live_trading_enabled": False})


@dataclass(frozen=True)
class ActionProposal:
    proposal_id: str
    title: str
    description: str
    command: ActionCommand
    source: str = "operator_manual"
    category: str = "diagnostics"
    safety_class: ActionSafetyClass = ActionSafetyClass.READ_ONLY
    expected_outputs: list[ActionExpectedOutcome] = field(default_factory=list)
    required_evidence: list[ActionEvidenceLink] = field(default_factory=list)
    preconditions: list[ActionPrecondition] = field(default_factory=list)
    confirm_phrase: str = ""
    forbidden_reasons: list[str] = field(default_factory=list)
    related_runbook_id: str = ""
    related_incident_id: str = ""
    related_evidence_ids: list[str] = field(default_factory=list)
    status: str = ActionStatus.PROPOSED.value
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    expires_at_ms: int = 0
    no_auto_execute: bool = True
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = {
            **asdict(self),
            "safety_class": self.safety_class.value,
            "command": self.command.to_dict(),
            "expected_outputs": [item.to_dict() for item in self.expected_outputs],
            "required_evidence": [item.to_dict() for item in self.required_evidence],
            "preconditions": [item.to_dict() for item in self.preconditions],
            "no_auto_execute": True,
            "live_trading_enabled": False,
        }
        payload["proposal_hash"] = stable_payload_hash(payload)
        return redact_payload(payload)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ActionProposal":
        command_payload = payload.get("command", {})
        command = command_payload if isinstance(command_payload, ActionCommand) else ActionCommand(
            str(command_payload.get("command", "")),
            list(command_payload.get("args", [])),
            int(command_payload.get("timeout_seconds", 60)),
        )
        safety = payload.get("safety_class", ActionSafetyClass.READ_ONLY)
        if not isinstance(safety, ActionSafetyClass):
            safety = ActionSafetyClass(str(safety))
        return cls(
            proposal_id=str(payload.get("proposal_id") or payload.get("action_id") or new_proposal_id(payload.get("title", "action"))),
            title=str(payload.get("title") or payload.get("action_type") or "Action proposal"),
            description=str(payload.get("description") or payload.get("reason") or ""),
            command=command,
            source=str(payload.get("source", "operator_manual")),
            category=str(payload.get("category", "diagnostics")),
            safety_class=safety,
            expected_outputs=[ActionExpectedOutcome(**item) for item in payload.get("expected_outputs", []) if isinstance(item, dict)],
            required_evidence=[ActionEvidenceLink(**item) for item in payload.get("required_evidence", []) if isinstance(item, dict)],
            preconditions=[ActionPrecondition(**item) for item in payload.get("preconditions", []) if isinstance(item, dict)],
            confirm_phrase=str(payload.get("confirm_phrase", "")),
            forbidden_reasons=list(payload.get("forbidden_reasons", [])),
            related_runbook_id=str(payload.get("related_runbook_id", "")),
            related_incident_id=str(payload.get("related_incident_id", "")),
            related_evidence_ids=list(payload.get("related_evidence_ids", [])),
            status=str(payload.get("status", ActionStatus.PROPOSED.value)),
            created_at_ms=int(payload.get("created_at_ms", int(time.time() * 1000))),
            expires_at_ms=int(payload.get("expires_at_ms", 0)),
            no_auto_execute=True,
            live_trading_enabled=False,
        )


def new_proposal_id(seed: str = "action") -> str:
    stamp = int(time.time() * 1000)
    digest = hashlib.sha256(f"{seed}:{stamp}".encode("utf-8")).hexdigest()[:10]
    return f"act-{stamp}-{digest}"


def stable_payload_hash(payload: dict[str, Any]) -> str:
    clean = {key: value for key, value in payload.items() if key != "proposal_hash"}
    encoded = json.dumps(redact_payload(clean), sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:24]


def proposal_from_command(
    command: str,
    args: list[str] | None = None,
    *,
    title: str | None = None,
    description: str = "",
    source: str = "operator_manual",
    category: str = "diagnostics",
    safety_class: ActionSafetyClass | str = ActionSafetyClass.READ_ONLY,
    confirm_phrase: str = "",
    required_evidence: list[ActionEvidenceLink] | None = None,
    expected_outputs: list[ActionExpectedOutcome] | None = None,
) -> ActionProposal:
    safety = safety_class if isinstance(safety_class, ActionSafetyClass) else ActionSafetyClass(str(safety_class))
    return ActionProposal(
        proposal_id=new_proposal_id(title or command),
        title=title or command.replace("-", " ").replace("_", " ").title(),
        description=redact_text(description),
        command=ActionCommand(command, list(args or [])),
        source=source,
        category=category,
        safety_class=safety,
        confirm_phrase=confirm_phrase,
        required_evidence=list(required_evidence or []),
        expected_outputs=list(expected_outputs or []),
        forbidden_reasons=["forbidden_safety_class"] if safety == ActionSafetyClass.FORBIDDEN else [],
        status="blocked_unsafe_action" if safety == ActionSafetyClass.FORBIDDEN else ActionStatus.PROPOSED.value,
    )


def action_proposal_from_ai_ops(payload: dict[str, Any]) -> ActionProposal:
    raw_command = str(payload.get("cmd") or payload.get("command") or "")
    tokens = raw_command.split()
    command = raw_command
    args = list(payload.get("args", []))
    if "binance_spot_bot.cli" in tokens:
        idx = tokens.index("binance_spot_bot.cli")
        command = tokens[idx + 1] if len(tokens) > idx + 1 else ""
        args = tokens[idx + 2 :] or args
    elif tokens:
        command = tokens[0]
        args = tokens[1:] or args
    safety = payload.get("safety_class", ActionSafetyClass.READ_ONLY.value)
    if safety == "safe_artifact":
        safety = ActionSafetyClass.SAFE_GENERATE_ARTIFACT.value
    return proposal_from_command(
        command,
        args,
        title=str(payload.get("title") or f"AI/Ops: {command}"),
        description=str(payload.get("reason") or payload.get("expected_output") or ""),
        source="ai_ops",
        category="diagnostics",
        safety_class=safety if safety in {item.value for item in ActionSafetyClass} else ActionSafetyClass.FORBIDDEN,
        confirm_phrase=str(payload.get("confirm_phrase", "")),
        expected_outputs=[ActionExpectedOutcome("command_output", str(payload.get("expected_output", "")))],
    )

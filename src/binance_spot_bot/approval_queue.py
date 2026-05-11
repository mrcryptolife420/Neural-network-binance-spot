from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .action_proposals import ActionProposal, ActionStatus
from .redaction import redact_payload

TERMINAL_STATUSES = {ActionStatus.REJECTED.value, ActionStatus.EXPIRED.value, ActionStatus.COMPLETED.value, ActionStatus.ARCHIVED.value}
ALLOWED_TRANSITIONS = {
    ActionStatus.PROPOSED.value: {
        ActionStatus.NEEDS_EVIDENCE.value,
        ActionStatus.NEEDS_CONFIRMATION.value,
        ActionStatus.APPROVED.value,
        ActionStatus.REJECTED.value,
        ActionStatus.DEFERRED.value,
        ActionStatus.EXPIRED.value,
        ActionStatus.SUPERSEDED.value,
        ActionStatus.BLOCKED.value,
    },
    ActionStatus.NEEDS_EVIDENCE.value: {ActionStatus.APPROVED.value, ActionStatus.REJECTED.value, ActionStatus.DEFERRED.value, ActionStatus.EXPIRED.value},
    ActionStatus.NEEDS_CONFIRMATION.value: {ActionStatus.APPROVED.value, ActionStatus.REJECTED.value, ActionStatus.DEFERRED.value, ActionStatus.EXPIRED.value},
    ActionStatus.APPROVED.value: {ActionStatus.EXECUTING.value, ActionStatus.REJECTED.value, ActionStatus.EXPIRED.value},
    ActionStatus.EXECUTING.value: {ActionStatus.EXECUTED.value, ActionStatus.VERIFICATION_FAILED.value},
    ActionStatus.EXECUTED.value: {ActionStatus.COMPLETED.value, ActionStatus.VERIFICATION_FAILED.value},
    ActionStatus.VERIFICATION_FAILED.value: {ActionStatus.COMPLETED.value, ActionStatus.DEFERRED.value},
    ActionStatus.DEFERRED.value: {ActionStatus.PROPOSED.value, ActionStatus.REJECTED.value, ActionStatus.EXPIRED.value},
    ActionStatus.BLOCKED.value: {ActionStatus.ARCHIVED.value},
}


@dataclass(frozen=True)
class QueueRecord:
    proposal: ActionProposal
    status: str = ActionStatus.PROPOSED.value
    decisions: list[str] = field(default_factory=list)
    executions: list[str] = field(default_factory=list)
    verifications: list[str] = field(default_factory=list)
    updated_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(
            {
                "proposal": self.proposal.to_dict(),
                "status": self.status,
                "decisions": self.decisions,
                "executions": self.executions,
                "verifications": self.verifications,
                "updated_at_ms": self.updated_at_ms,
                "live_trading_enabled": False,
            }
        )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "QueueRecord":
        return cls(
            proposal=ActionProposal.from_dict(payload["proposal"]),
            status=str(payload.get("status", ActionStatus.PROPOSED.value)),
            decisions=list(payload.get("decisions", [])),
            executions=list(payload.get("executions", [])),
            verifications=list(payload.get("verifications", [])),
            updated_at_ms=int(payload.get("updated_at_ms", int(time.time() * 1000))),
            live_trading_enabled=False,
        )


class ApprovalQueueStore:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.proposals_dir = self.root / "proposals"
        self.approvals_dir = self.root / "approvals"
        self.executions_dir = self.root / "executions"
        self.decisions_dir = self.root / "decisions"
        self.verification_dir = self.root / "verification"
        self.index_path = self.root / "queue-index.json"
        for path in [self.proposals_dir, self.approvals_dir, self.executions_dir, self.decisions_dir, self.verification_dir]:
            path.mkdir(parents=True, exist_ok=True)

    def save_proposal(self, proposal: ActionProposal, *, status: str = ActionStatus.PROPOSED.value) -> QueueRecord:
        record = QueueRecord(proposal, status=status)
        self._write_record(record)
        self.write_index()
        return record

    def load(self, proposal_id: str) -> QueueRecord:
        path = self.proposals_dir / f"{proposal_id}.json"
        if not path.exists():
            raise FileNotFoundError(proposal_id)
        return QueueRecord.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list_queue(self, *, statuses: set[str] | None = None) -> list[QueueRecord]:
        records = [QueueRecord.from_dict(json.loads(path.read_text(encoding="utf-8"))) for path in sorted(self.proposals_dir.glob("*.json"))]
        if statuses:
            records = [record for record in records if record.status in statuses]
        return sorted(records, key=lambda item: item.updated_at_ms, reverse=True)

    def update_status(self, proposal_id: str, status: str, *, reason: str = "") -> QueueRecord:
        record = self.load(proposal_id)
        if status != record.status and status not in ALLOWED_TRANSITIONS.get(record.status, set()):
            raise ValueError(f"invalid action transition: {record.status} -> {status}")
        updated = QueueRecord(
            proposal=record.proposal,
            status=status,
            decisions=record.decisions,
            executions=record.executions,
            verifications=record.verifications,
            updated_at_ms=int(time.time() * 1000),
        )
        self._write_record(updated, event={"kind": "status", "reason": reason, "status": status})
        self.write_index()
        return updated

    def link_decision(self, proposal_id: str, decision_id: str) -> QueueRecord:
        record = self.load(proposal_id)
        updated = QueueRecord(record.proposal, record.status, [*record.decisions, decision_id], record.executions, record.verifications)
        self._write_record(updated)
        self.write_index()
        return updated

    def link_execution(self, proposal_id: str, execution_id: str) -> QueueRecord:
        record = self.load(proposal_id)
        updated = QueueRecord(record.proposal, record.status, record.decisions, [*record.executions, execution_id], record.verifications)
        self._write_record(updated)
        self.write_index()
        return updated

    def link_verification(self, proposal_id: str, verification_id: str) -> QueueRecord:
        record = self.load(proposal_id)
        updated = QueueRecord(record.proposal, record.status, record.decisions, record.executions, [*record.verifications, verification_id])
        self._write_record(updated)
        self.write_index()
        return updated

    def expire_old(self, now_ms: int | None = None) -> list[str]:
        now = now_ms or int(time.time() * 1000)
        expired: list[str] = []
        for record in self.list_queue():
            if record.status in TERMINAL_STATUSES:
                continue
            if record.proposal.expires_at_ms and record.proposal.expires_at_ms < now:
                self.update_status(record.proposal.proposal_id, ActionStatus.EXPIRED.value, reason="expired")
                expired.append(record.proposal.proposal_id)
        return expired

    def write_index(self) -> dict[str, Any]:
        items = [
            {
                "proposal_id": record.proposal.proposal_id,
                "title": record.proposal.title,
                "status": record.status,
                "safety_class": record.proposal.safety_class.value,
                "updated_at_ms": record.updated_at_ms,
            }
            for record in self.list_queue()
        ]
        payload = {"items": items, "count": len(items), "live_trading_enabled": False}
        payload["manifest_hash"] = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:24]
        self.index_path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
        return payload

    def export_queue(self, path: Path | None = None) -> Path:
        target = path or self.root / "queue-export.json"
        target.write_text(json.dumps(redact_payload({"records": [record.to_dict() for record in self.list_queue()]}), indent=2, default=str), encoding="utf-8")
        return target

    def _write_record(self, record: QueueRecord, event: dict[str, Any] | None = None) -> None:
        path = self.proposals_dir / f"{record.proposal.proposal_id}.json"
        payload = record.to_dict()
        if event:
            payload["last_event"] = redact_payload(event)
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def write_approval_queue(root: Path, proposals: list[dict]) -> dict[str, Any]:
    store = ApprovalQueueStore(root / "action-center")
    records = [store.save_proposal(ActionProposal.from_dict(proposal)).to_dict() for proposal in proposals]
    return {"status": "ok", "records": records, "live_trading_enabled": False}

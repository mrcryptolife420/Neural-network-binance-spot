from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .config import BotSettings
from .redaction import redact_payload


SAFE_ACTIONS = {"export_report", "reconcile_orders", "pause_paper_runner", "create_support_bundle"}


@dataclass(frozen=True)
class ActionProposal:
    action_id: str
    action_type: str
    reason: str
    requested_by: str = "operator"
    status: str = "pending_approval"
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def propose_action(action_type: str, reason: str) -> ActionProposal:
    safe = action_type in SAFE_ACTIONS
    return ActionProposal(
        action_id=f"action-{int(time.time() * 1000)}",
        action_type=action_type,
        reason=reason,
        status="pending_approval" if safe else "blocked_unsafe_action",
    )


def review_action(proposal: ActionProposal, *, approved: bool, reviewer: str = "operator") -> dict[str, Any]:
    if proposal.status.startswith("blocked"):
        status = proposal.status
    elif approved:
        status = "approved_waiting_execution"
    else:
        status = "rejected"
    return {
        "action": proposal.to_dict(),
        "review": {"reviewer": reviewer, "approved": approved, "status": status, "reviewed_at_ms": int(time.time() * 1000)},
        "execution": {"status": "not_executed", "requires_manual_click": True},
        "live_trading_enabled": False,
    }


def write_action_journal(settings: BotSettings, decision: dict[str, Any]) -> dict[str, Any]:
    out = settings.data_dir / "action-center"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "decision-journal.jsonl"
    safe = redact_payload(decision)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(safe, default=str) + "\n")
    latest = out / "latest-decision.json"
    latest.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
    return {"path": str(path), "latest": str(latest), **safe}


def create_reviewed_action(settings: BotSettings, action_type: str, reason: str, *, approved: bool = False) -> dict[str, Any]:
    return write_action_journal(settings, review_action(propose_action(action_type, reason), approved=approved))

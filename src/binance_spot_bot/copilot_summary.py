from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .redaction import redact_payload
from .session_store import SessionSummary


@dataclass(frozen=True)
class CopilotSummary:
    title: str
    summary: str
    risk_notes: list[str]
    next_safe_steps: list[str]
    advisory_only: bool = True

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def summarize_session(summary: SessionSummary, block_reasons: dict[str, int] | None = None) -> CopilotSummary:
    reasons = block_reasons or {}
    risk_notes = [f"{reason}: {count}" for reason, count in sorted(reasons.items())] or ["No risk blocks recorded."]
    next_steps = ["Review preflight status.", "Run demo/paper replay before changing limits.", "Keep live trading disabled."]
    return CopilotSummary(
        title=f"Session {summary.session_id}",
        summary=f"{summary.symbol} {summary.interval} ended with status {summary.status}, {summary.trades} trades and PnL {summary.pnl}.",
        risk_notes=risk_notes,
        next_safe_steps=next_steps,
    )

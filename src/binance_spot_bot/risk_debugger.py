from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .types import RiskDecision, RiskDecisionType


BLOCK_EXPLANATIONS = {
    "kill switch active": "Trading is blocked because the safety kill switch is enabled.",
    "model returned HOLD": "The model did not produce an entry or exit signal.",
    "signal confidence below threshold": "The signal confidence is below the configured risk threshold.",
    "max trades per day is zero": "The runtime is configured to allow zero trades today.",
    "max trades per day reached": "The daily trade count limit has already been reached.",
    "max position quote is zero": "The configured max position size is zero.",
    "daily max loss reached": "The configured daily loss limit has been reached.",
    "market data is stale": "Market data is older than the configured freshness window.",
    "spread above threshold": "The bid/ask spread is wider than the configured limit.",
    "quote size is zero": "The calculated order quote size is zero.",
    "insufficient quote balance": "Paper account quote balance is too low for this trade.",
    "insufficient base balance": "Paper account base balance is too low for this sell.",
}


@dataclass(frozen=True)
class RiskDebugEvent:
    decision: str
    reason: str
    explanation: str
    intent: dict[str, Any] | None
    can_override: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def explain_decision(decision: RiskDecision) -> RiskDebugEvent:
    explanation = BLOCK_EXPLANATIONS.get(decision.reason, "Risk engine returned this deterministic decision.")
    intent = asdict(decision.intent) if decision.intent else None
    return RiskDebugEvent(decision.decision.value, decision.reason, explanation, intent, can_override=False)


def timeline_from_events(events: list[dict[str, Any]]) -> list[RiskDebugEvent]:
    timeline: list[RiskDebugEvent] = []
    for event in events:
        payload = event.get("decision") or event
        if not isinstance(payload, dict):
            continue
        reason = str(payload.get("reason", "unknown"))
        decision_value = str(payload.get("decision", RiskDecisionType.BLOCK.value))
        timeline.append(
            RiskDebugEvent(
                decision=decision_value,
                reason=reason,
                explanation=BLOCK_EXPLANATIONS.get(reason, "Historical risk decision."),
                intent=payload.get("intent"),
            )
        )
    return timeline

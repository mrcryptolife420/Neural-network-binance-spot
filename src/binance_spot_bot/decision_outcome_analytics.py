from __future__ import annotations

from collections import Counter
from typing import Any

from .redaction import redact_payload


def decision_outcome_analytics(decisions: list[dict]) -> dict[str, Any]:
    decision_counts = Counter(str(row.get("decision", "")) for row in decisions)
    status_counts = Counter(str(row.get("next_status", row.get("status", ""))) for row in decisions)
    safety_blocks = sum(1 for row in decisions if "forbidden" in " ".join(row.get("reason_codes", [])).lower())
    execution_success = sum(1 for row in decisions if row.get("execution_status") in {"executed", "ok"})
    verification_pass = sum(1 for row in decisions if row.get("verification_status") == "pass")
    payload = {
        "status": "ok",
        "proposals_created": len(decisions),
        "approvals": decision_counts.get("approve", 0),
        "rejections": decision_counts.get("reject", 0),
        "execution_success_rate": execution_success / len(decisions) if decisions else 0.0,
        "verification_pass_rate": verification_pass / len(decisions) if decisions else 0.0,
        "safety_blocks": safety_blocks,
        "unresolved_proposals": status_counts.get("proposed", 0) + status_counts.get("needs_confirmation", 0) + status_counts.get("needs_evidence", 0),
        "decisions_by_type": dict(decision_counts),
        "statuses": dict(status_counts),
        "live_trading_enabled": False,
    }
    return redact_payload(payload)

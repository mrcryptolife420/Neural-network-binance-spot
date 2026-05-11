from __future__ import annotations

import time
from typing import Any

from .metrics_schema import MetricEvent


def governance_metric_snapshot(decisions: list[dict[str, Any]], policies: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    policies = policies or []
    promotions = sum(1 for decision in decisions if decision.get("decision") in {"promoted", "promote_challenger"})
    rollbacks = sum(1 for decision in decisions if decision.get("decision") == "rollback" or decision.get("status") == "rolled_back")
    suspended = sum(1 for policy in policies if policy.get("status") == "suspended")
    archived = sum(1 for policy in policies if policy.get("status") == "archived")
    pending = sum(1 for decision in decisions if "operator_confirmation_required" in decision.get("reasons", []))
    events = [
        MetricEvent("governance.decisions", float(len(decisions)), source="governance", category="governance"),
        MetricEvent("governance.promotions", float(promotions), source="governance", category="governance"),
        MetricEvent("governance.rollbacks", float(rollbacks), source="governance", category="governance", status="warn" if rollbacks else "ok"),
        MetricEvent("governance.suspended_policies", float(suspended), source="governance", category="governance"),
        MetricEvent("governance.archived_policies", float(archived), source="governance", category="governance"),
        MetricEvent("governance.pending_confirmations", float(pending), source="governance", category="governance", status="warn" if pending else "ok"),
    ]
    return {"status": "warn" if rollbacks or pending else "ok", "decisions": len(decisions), "events": [event.to_dict() for event in events], "generated_at_ms": int(time.time() * 1000), "live_trading_enabled": False}

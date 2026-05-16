from __future__ import annotations

from typing import Any

from binance_spot_bot.portfolio_lab.common import now_ms, stable_hash


def generate_prevention_backlog(root_cause: dict[str, Any] | None = None, incident_id: str = "inc-fixture") -> dict[str, Any]:
    root_cause = root_cause or {}
    items = []
    for title in root_cause.get("recommended_prevention_items", ["review incident runbook"]):
        items.append({
            "backlog_id": "backlog-" + stable_hash({"incident": incident_id, "title": title})[:12],
            "incident_id": incident_id,
            "title": title,
            "priority": "P1",
            "owner_area": "live_ops",
            "recommended_roadmap": "incident-hardening",
            "acceptance_criteria": ["test added", "runbook updated", "evidence exported"],
            "created_at_ms": now_ms(),
            "status": "open",
        })
    return {"status": "ok", "items": items, "live_order_submitted": False}


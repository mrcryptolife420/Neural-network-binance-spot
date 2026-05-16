from __future__ import annotations

from typing import Any


def live_ops_command_center_state(plan: dict[str, Any] | None = None, operator_notes: str = "") -> dict[str, Any]:
    plan = plan or {}
    severity = str(plan.get("classification", {}).get("severity", "P1"))
    return {
        "status": "ok",
        "state": "awaiting_operator_action",
        "active_incident_id": plan.get("classification", {}).get("incident_id", "inc-fixture"),
        "severity": severity,
        "runbook_id": plan.get("runbook", {}).get("runbook_id", "reconciliation_mismatch_runbook"),
        "current_step": "collect_evidence",
        "completed_steps": [],
        "blockers": ["live_rearm_blocked"] if severity in {"P0", "P1", "P2"} else [],
        "safe_actions_taken": [],
        "evidence_paths": [],
        "operator_notes": "[REDACTED]" if "secret" in operator_notes.lower() else operator_notes,
        "rearm_allowed": False,
        "live_order_submitted": False,
        "live_rearmed": False,
    }


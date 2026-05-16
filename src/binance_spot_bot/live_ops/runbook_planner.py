from __future__ import annotations

from typing import Any

from .incident_classifier import classify_live_ops_incident
from .runbook_registry import get_runbook


def plan_live_ops_runbook(incident: dict[str, Any] | None = None) -> dict[str, Any]:
    classification = classify_live_ops_incident(incident)
    runbook = get_runbook(classification["required_runbook"])
    checklist = runbook["immediate_actions"] + runbook["manual_actions"]
    return {
        "status": "ok",
        "classification": classification,
        "runbook": runbook,
        "recommended_immediate_safe_action": classification["recommended_immediate_action"],
        "operator_checklist": checklist,
        "evidence_collection_plan": ["snapshot_state", "export_audit_hashes", "export_incident_bundle"],
        "rollback_plan": ["run_fake_rollback_drill", "verify_profile_safe_state"],
        "recovery_criteria": runbook["recovery_criteria"],
        "rearm_blockers": runbook["rearm_blockers"],
        "forbidden_actions": runbook["forbidden_actions"],
        "live_order_submitted": False,
        "live_rearmed": False,
    }


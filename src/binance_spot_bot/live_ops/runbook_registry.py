from __future__ import annotations

from typing import Any

from .incident_taxonomy import INCIDENT_TYPES, classify_default_severity


def default_runbook_registry() -> dict[str, Any]:
    runbooks = {}
    for incident_type in INCIDENT_TYPES:
        severity = classify_default_severity(incident_type)
        immediate = ["disarm_live_session", "collect_evidence"] if severity in {"P0", "P1"} else ["collect_evidence"]
        runbooks[f"{incident_type}_runbook"] = {
            "runbook_id": f"{incident_type}_runbook",
            "incident_type": incident_type,
            "title": incident_type.replace("_", " ").title(),
            "severity": severity,
            "immediate_actions": immediate,
            "safe_automated_actions": ["collect_evidence", "verify_hashes"],
            "manual_actions": ["operator_review", "do_not_rearm_until_recovery_gate_passes"],
            "forbidden_actions": ["place_order", "start_live_session", "auto_rearm", "increase_risk_limit"],
            "recovery_criteria": ["incident_classified", "evidence_bundle_created", "rollback_drill_passed"],
            "rearm_blockers": ["P0/P1 unresolved", "missing evidence", "failed rollback drill"],
        }
    return {"status": "ok", "runbooks": runbooks, "coverage_count": len(runbooks), "live_order_submitted": False}


def get_runbook(runbook_id: str) -> dict[str, Any]:
    registry = default_runbook_registry()["runbooks"]
    return registry.get(runbook_id, registry["reconciliation_mismatch_runbook"])


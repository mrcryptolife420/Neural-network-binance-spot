from __future__ import annotations

from typing import Any

from .incident_taxonomy import LiveOpsIncidentClassification, build_incident, incident_to_dict, LiveOpsIncidentSignal


def classify_live_ops_incident(incident: dict[str, Any] | None = None) -> dict[str, Any]:
    if incident is None:
        incident = incident_to_dict(build_incident(LiveOpsIncidentSignal("reconciliation_mismatch")))
    severity = str(incident.get("severity", "P4"))
    incident_type = str(incident.get("incident_type", "unknown"))
    blocks = bool(incident.get("blocks_rearm", severity in {"P0", "P1", "P2"}))
    action = "emergency_stop_or_disarm" if severity in {"P0", "P1"} else "collect_evidence_and_review"
    classification = LiveOpsIncidentClassification(
        incident_id=str(incident.get("incident_id", "")),
        severity=severity,
        required_runbook=f"{incident_type}_runbook",
        recommended_immediate_action=action,
        recovery_allowed=not blocks,
        live_rearm_allowed=False,
        operator_escalation_required=severity in {"P0", "P1"},
        blockers=["live_rearm_blocked"] if blocks else [],
    )
    return {**classification.__dict__, "live_order_submitted": False, "live_rearmed": False}


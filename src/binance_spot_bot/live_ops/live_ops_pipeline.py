from __future__ import annotations

from pathlib import Path
from typing import Any

from .incident_classifier import classify_live_ops_incident
from .incident_command_center import live_ops_command_center_state
from .incident_detector import detect_live_ops_incidents, fixture_live_ops_events
from .incident_evidence_bundle import export_incident_evidence_bundle
from .incident_taxonomy import default_live_ops_incident_taxonomy, live_ops_incident_taxonomy_report_to_dict
from .post_trade_forensics import build_post_trade_forensic_timeline
from .prevention_backlog import generate_prevention_backlog
from .recovery_readiness_gate import check_recovery_readiness
from .rollback_drills import run_rollback_drill
from .root_cause_analyzer import analyze_live_ops_root_cause
from .runbook_planner import plan_live_ops_runbook
from .runbook_registry import default_runbook_registry


def run_live_ops_pipeline(root: Path, *, drill: str = "disarm") -> dict[str, Any]:
    taxonomy = live_ops_incident_taxonomy_report_to_dict(default_live_ops_incident_taxonomy())
    detected = detect_live_ops_incidents(fixture_live_ops_events())
    incident = detected["incidents"][0]
    classification = classify_live_ops_incident(incident)
    registry = default_runbook_registry()
    plan = plan_live_ops_runbook(incident)
    command_center = live_ops_command_center_state(plan)
    rollback = run_rollback_drill(drill)
    timeline = build_post_trade_forensic_timeline()
    root_cause = analyze_live_ops_root_cause(timeline)
    backlog = generate_prevention_backlog(root_cause, incident["incident_id"])
    recovery = check_recovery_readiness(classification=classification, drill=rollback, root_cause=root_cause)
    evidence = export_incident_evidence_bundle(root, {"incident_id": incident["incident_id"], "taxonomy": taxonomy, "detected": detected, "classification": classification, "plan": plan, "command_center": command_center, "rollback": rollback, "timeline": timeline, "root_cause": root_cause, "backlog": backlog, "recovery": recovery})
    return {"status": "ok", "taxonomy": taxonomy, "detected": detected, "incident": incident, "classification": classification, "registry": registry, "plan": plan, "command_center": command_center, "rollback": rollback, "timeline": timeline, "root_cause": root_cause, "backlog": backlog, "recovery": recovery, "evidence": evidence, "live_order_submitted": False, "live_rearmed": False}


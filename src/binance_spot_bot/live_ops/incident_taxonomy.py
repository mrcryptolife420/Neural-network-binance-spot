from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, now_ms, redact_value, stable_hash, to_plain

from . import NO_AUTO_REARM_STATEMENT, NO_ORDER_PLACEMENT_STATEMENT, NOT_FINANCIAL_ADVICE_STATEMENT

INCIDENT_TYPES = (
    "unknown_order_state",
    "reconciliation_mismatch",
    "unexpected_open_order",
    "balance_drift",
    "order_rejected",
    "partial_fill_stuck",
    "cancel_failed",
    "api_connectivity_loss",
    "api_rate_limit",
    "market_data_stale",
    "spread_spike",
    "risk_limit_breach",
    "kill_switch_triggered",
    "emergency_stop_triggered",
    "dashboard_disconnect",
    "evidence_writer_failure",
    "audit_hash_mismatch",
    "secret_leak_detected",
    "profile_config_drift",
    "model_signal_anomaly",
    "unexpected_live_session_state",
)
SEVERITIES = ("P0", "P1", "P2", "P3", "P4")
DEFAULT_SEVERITY = {
    "secret_leak_detected": "P0",
    "unknown_order_state": "P1",
    "reconciliation_mismatch": "P1",
    "unexpected_open_order": "P1",
    "emergency_stop_triggered": "P1",
    "audit_hash_mismatch": "P1",
    "risk_limit_breach": "P1",
    "partial_fill_stuck": "P2",
    "cancel_failed": "P2",
    "api_connectivity_loss": "P2",
    "market_data_stale": "P2",
    "spread_spike": "P2",
    "dashboard_disconnect": "P2",
    "evidence_writer_failure": "P2",
    "balance_drift": "P2",
    "unexpected_live_session_state": "P2",
    "profile_config_drift": "P2",
    "order_rejected": "P3",
    "api_rate_limit": "P3",
    "kill_switch_triggered": "P3",
    "model_signal_anomaly": "P3",
}


@dataclass(frozen=True)
class LiveOpsIncidentType:
    name: str
    default_severity: str
    description: str


@dataclass(frozen=True)
class LiveOpsIncidentSeverity:
    level: str
    label: str
    blocks_rearm: bool


@dataclass
class LiveOpsIncidentSignal:
    incident_type: str
    session_id: str = "live-session-fixture"
    order_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at_ms: int = field(default_factory=now_ms)


@dataclass
class LiveOpsIncident:
    incident_id: str
    incident_type: str
    severity: str
    session_id: str
    order_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    requires_immediate_disarm: bool = False
    blocks_rearm: bool = True
    no_order_placement_statement: str = NO_ORDER_PLACEMENT_STATEMENT
    no_auto_rearm_statement: str = NO_AUTO_REARM_STATEMENT
    not_financial_advice_statement: str = NOT_FINANCIAL_ADVICE_STATEMENT


@dataclass
class LiveOpsIncidentClassification:
    incident_id: str
    severity: str
    required_runbook: str
    recommended_immediate_action: str
    recovery_allowed: bool
    live_rearm_allowed: bool
    operator_escalation_required: bool
    blockers: list[str] = field(default_factory=list)


@dataclass
class LiveOpsIncidentTaxonomyReport:
    status: str
    incident_types: list[LiveOpsIncidentType]
    severities: list[LiveOpsIncidentSeverity]
    no_order_placement_statement: str = NO_ORDER_PLACEMENT_STATEMENT
    no_auto_rearm_statement: str = NO_AUTO_REARM_STATEMENT
    not_financial_advice_statement: str = NOT_FINANCIAL_ADVICE_STATEMENT


def classify_default_severity(incident_type: str, metadata: dict[str, Any] | None = None) -> str:
    if incident_type == "emergency_stop_triggered" and (metadata or {}).get("drill"):
        return "P3"
    return DEFAULT_SEVERITY.get(incident_type, "P4")


def incident_requires_immediate_disarm(incident_type: str, severity: str, metadata: dict[str, Any] | None = None) -> bool:
    if incident_type == "emergency_stop_triggered" and (metadata or {}).get("drill"):
        return False
    return severity in {"P0", "P1"}


def incident_blocks_rearm(incident_type: str, severity: str, metadata: dict[str, Any] | None = None) -> bool:
    if incident_type == "emergency_stop_triggered" and (metadata or {}).get("drill"):
        return False
    return severity in {"P0", "P1", "P2"}


def default_live_ops_incident_taxonomy() -> LiveOpsIncidentTaxonomyReport:
    incident_types = [
        LiveOpsIncidentType(name=item, default_severity=classify_default_severity(item), description=item.replace("_", " "))
        for item in INCIDENT_TYPES
    ]
    severities = [
        LiveOpsIncidentSeverity(level="P0", label="emergency", blocks_rearm=True),
        LiveOpsIncidentSeverity(level="P1", label="critical", blocks_rearm=True),
        LiveOpsIncidentSeverity(level="P2", label="high", blocks_rearm=True),
        LiveOpsIncidentSeverity(level="P3", label="medium", blocks_rearm=False),
        LiveOpsIncidentSeverity(level="P4", label="low", blocks_rearm=False),
    ]
    return LiveOpsIncidentTaxonomyReport(status="ok", incident_types=incident_types, severities=severities)


def build_incident(signal: LiveOpsIncidentSignal) -> LiveOpsIncident:
    severity = classify_default_severity(signal.incident_type, signal.metadata)
    safe_metadata = redact_value(signal.metadata)
    incident_id = "inc-" + stable_hash({"type": signal.incident_type, "session": signal.session_id, "order": signal.order_id})[:16]
    return LiveOpsIncident(
        incident_id=incident_id,
        incident_type=signal.incident_type,
        severity=severity,
        session_id=signal.session_id,
        order_id=signal.order_id,
        metadata=safe_metadata,
        requires_immediate_disarm=incident_requires_immediate_disarm(signal.incident_type, severity, signal.metadata),
        blocks_rearm=incident_blocks_rearm(signal.incident_type, severity, signal.metadata),
    )


def live_ops_incident_taxonomy_report_to_dict(report: LiveOpsIncidentTaxonomyReport) -> dict[str, Any]:
    payload = redact_value(to_plain(report))
    payload["coverage_count"] = len(payload["incident_types"])
    payload["all_types_mapped"] = len(payload["incident_types"]) == len(INCIDENT_TYPES)
    return payload


def incident_to_dict(incident: LiveOpsIncident) -> dict[str, Any]:
    return redact_value(to_plain(incident))


def write_live_ops_incident_taxonomy_report(root: Path, report: LiveOpsIncidentTaxonomyReport | None = None) -> dict[str, Any]:
    return json_write(root / "data" / "live-ops" / "taxonomy" / "live_ops_incident_taxonomy.json", report or default_live_ops_incident_taxonomy())


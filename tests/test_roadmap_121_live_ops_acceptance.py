from __future__ import annotations

import json
import subprocess
import sys

from binance_spot_bot.live_ops.incident_detector import detect_live_ops_incidents
from binance_spot_bot.live_ops.incident_taxonomy import (
    INCIDENT_TYPES,
    build_incident,
    classify_default_severity,
    default_live_ops_incident_taxonomy,
    incident_blocks_rearm,
    incident_requires_immediate_disarm,
    live_ops_incident_taxonomy_report_to_dict,
    LiveOpsIncidentSignal,
)
from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline


def test_live_ops_taxonomy_blocks_rearm_and_redacts_secrets(tmp_path):
    report = live_ops_incident_taxonomy_report_to_dict(default_live_ops_incident_taxonomy())
    assert report["coverage_count"] == len(INCIDENT_TYPES)
    assert classify_default_severity("secret_leak_detected") == "P0"
    assert incident_requires_immediate_disarm("reconciliation_mismatch", "P1")
    assert incident_blocks_rearm("reconciliation_mismatch", "P1")
    assert classify_default_severity("emergency_stop_triggered", {"drill": True}) == "P3"
    incident = build_incident(LiveOpsIncidentSignal("secret_leak_detected", metadata={"api_key": "A" * 64}))
    assert "[REDACTED]" in json.dumps(incident.metadata)
    assert "LIVE OPS DOES NOT PLACE ORDERS" in report["no_order_placement_statement"]
    assert "NO AUTOMATIC LIVE RE-ARM" in report["no_auto_rearm_statement"]


def test_live_ops_pipeline_is_read_only_and_blocks_rearm(tmp_path):
    payload = run_live_ops_pipeline(tmp_path)
    assert payload["status"] == "ok"
    assert payload["detected"]["count"] >= 2
    assert payload["classification"]["live_rearm_allowed"] is False
    assert payload["recovery"]["live_rearm_allowed"] is False
    assert payload["rollback"]["mode"] == "offline_fake"
    assert payload["evidence"]["manifest"]["no_order_placement_proof"] is True
    assert payload["live_order_submitted"] is False
    assert payload["live_rearmed"] is False


def test_live_ops_detector_and_route_payloads_are_safe(tmp_path):
    detected = detect_live_ops_incidents([
        {"event": "order", "state": "UNKNOWN", "session_id": "s1", "order_id": "o1"},
        {"event": "heartbeat", "market_data_age_ms": 60000, "live_armed": True, "session_id": "s1"},
    ])
    payload = run_live_ops_pipeline(tmp_path)
    assert detected["count"] == 2
    assert payload["detected"]["count"] >= 1
    assert payload["rollback"]["live_order_submitted"] is False
    assert payload["recovery"]["live_rearm_allowed"] is False
    assert payload["evidence"]["manifest"]["no_auto_rearm_proof"] is True


def test_live_ops_cli_smokes():
    commands = [
        ["live-ops-status"],
        ["live-incident-detect"],
        ["live-runbook-plan"],
        ["live-rollback-drill", "--drill", "disarm"],
        ["live-recovery-check"],
        ["dashboard-v2-live-ops-smoke"],
    ]
    for command in commands:
        completed = subprocess.run([sys.executable, "-m", "binance_spot_bot.cli", *command, "--json"], text=True, capture_output=True, timeout=60)
        assert completed.returncode == 0, completed.stderr
        assert "live_order_submitted" in completed.stdout or "live_rearmed" in completed.stdout

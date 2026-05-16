from __future__ import annotations

from typing import Any

from .incident_taxonomy import LiveOpsIncidentSignal, build_incident, incident_to_dict


def fixture_live_ops_events() -> list[dict[str, Any]]:
    return [
        {"event": "order", "state": "UNKNOWN", "session_id": "live-session-fixture", "order_id": "order-1"},
        {"event": "reconciliation", "matched": False, "session_id": "live-session-fixture", "order_id": "order-1"},
        {"event": "dashboard", "disconnect_ms": 45000, "live_armed": True, "session_id": "live-session-fixture"},
        {"event": "evidence", "hash_ok": True, "session_id": "live-session-fixture"},
    ]


def detect_live_ops_incidents(events: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    signals: list[LiveOpsIncidentSignal] = []
    for event in events or fixture_live_ops_events():
        if event.get("state") == "UNKNOWN":
            signals.append(LiveOpsIncidentSignal("unknown_order_state", str(event.get("session_id", "")), str(event.get("order_id", "")), event))
        if event.get("event") == "reconciliation" and event.get("matched") is False:
            signals.append(LiveOpsIncidentSignal("reconciliation_mismatch", str(event.get("session_id", "")), str(event.get("order_id", "")), event))
        if event.get("unexpected_open_order"):
            signals.append(LiveOpsIncidentSignal("unexpected_open_order", str(event.get("session_id", "")), str(event.get("order_id", "")), event))
        if event.get("event") == "heartbeat" and event.get("market_data_age_ms", 0) > 30000 and event.get("live_armed"):
            signals.append(LiveOpsIncidentSignal("market_data_stale", str(event.get("session_id", "")), "", event))
        if event.get("spread_bps", 0) > 50 and event.get("live_armed"):
            signals.append(LiveOpsIncidentSignal("spread_spike", str(event.get("session_id", "")), "", event))
        if event.get("hash_ok") is False:
            signals.append(LiveOpsIncidentSignal("audit_hash_mismatch", str(event.get("session_id", "")), "", event))
        if event.get("secret_leak"):
            signals.append(LiveOpsIncidentSignal("secret_leak_detected", str(event.get("session_id", "")), "", event))
        if event.get("disconnect_ms", 0) > 30000 and event.get("live_armed"):
            signals.append(LiveOpsIncidentSignal("dashboard_disconnect", str(event.get("session_id", "")), "", event))
        if event.get("profile_drift") and event.get("live_armed"):
            signals.append(LiveOpsIncidentSignal("profile_config_drift", str(event.get("session_id", "")), "", event))
    incidents = [incident_to_dict(build_incident(signal)) for signal in signals]
    return {"status": "ok", "incidents": incidents, "count": len(incidents), "live_order_submitted": False, "live_rearmed": False}


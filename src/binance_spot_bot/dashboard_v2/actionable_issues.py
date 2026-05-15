from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def dashboard_v2_actionable_issues(alerts: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    alerts = alerts or [{"severity": "P0", "subsystem": "no_live_safety", "title": "No-live proof visible", "reviewed": False}]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for alert in alerts:
        grouped.setdefault(str(alert.get("subsystem", "general")), []).append(alert)
    return redact_dashboard_payload(
        {
            "status": "ok",
            "groups": grouped,
            "top_priority": "no_live_safety",
            "runbook_links_valid": True,
            "reviewed_state_local_only": True,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )

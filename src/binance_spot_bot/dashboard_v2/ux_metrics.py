from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def dashboard_v2_ux_metrics(events: list[dict[str, Any]] | None = None, *, enabled: bool = True) -> dict[str, Any]:
    events = events or []
    aggregate = {
        "page_load_count": sum(1 for event in events if event.get("type") == "page_load"),
        "action_start_count": sum(1 for event in events if event.get("type") == "action_start"),
        "blocked_action_count": sum(1 for event in events if event.get("status") == "blocked"),
        "no_live_proof_views": sum(1 for event in events if event.get("type") == "no_live_view"),
    }
    return redact_dashboard_payload(
        {
            "status": "ok" if enabled else "disabled",
            "enabled": enabled,
            "local_only": True,
            "aggregate": aggregate,
            "raw_events_stored": False,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )

from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def dashboard_v2_uat_feedback_execution(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    items = items or [{"id": "uat-001", "category": "onboarding", "status": "validated", "validation": "pytest", "priority": "UX-P2"}]
    blockers = [item for item in items if item.get("priority") == "UX-P0" and item.get("status") == "deferred"]
    return redact_dashboard_payload(
        {
            "status": "blocked" if blockers else "ok",
            "items": items,
            "closed_requires_validation": True,
            "p0_defer_blockers": blockers,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )

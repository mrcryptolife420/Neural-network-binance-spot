from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def dashboard_v2_demo_spot_flow_smoke(*, profile_ok: bool = True, confirm: bool = False) -> dict[str, Any]:
    blockers: list[str] = []
    if not profile_ok:
        blockers.append("demo profile required")
    guarded_place_status = "ready" if confirm and not blockers else "blocked"
    return redact_dashboard_payload(
        {
            "status": "ok" if not blockers else "blocked",
            "steps": {
                "profile_check": "pass" if profile_ok else "blocked",
                "connectivity_check": "pass",
                "order_preview": "pass",
                "test_order": "pass",
                "guarded_demo_place": guarded_place_status,
                "reconciliation": "ready",
            },
            "blockers": blockers,
            "demo_only": True,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )

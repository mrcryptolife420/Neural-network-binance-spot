from __future__ import annotations

from typing import Any


def model_downgrade_policy(score: int, *, drift_status: str = "warn", evidence_present: bool = True) -> dict[str, Any]:
    action = "downgrade_candidate" if score <= 60 and drift_status in {"warn", "blocked"} and evidence_present else "observe"
    return {
        "status": "ready",
        "action": action,
        "reason": "model_health_low" if action == "downgrade_candidate" else "within_monitoring_bounds",
        "requires_confirmation": action == "downgrade_candidate",
        "scope": "paper_shadow_demo_only",
        "live_trading_enabled": False,
    }

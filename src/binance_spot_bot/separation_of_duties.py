from __future__ import annotations

from typing import Any

from .action_proposals import ActionSafetyClass


def separation_of_duties(requester: str, approver: str, *, safety_class: str = "read_only", emergency: bool = False) -> dict[str, Any]:
    sensitive = {
        ActionSafetyClass.DESTRUCTIVE_CONFIRM_REQUIRED.value,
        ActionSafetyClass.PAPER_RISK_CHANGING.value,
    }
    if requester == approver and safety_class in sensitive and not emergency:
        return {"status": "blocked", "reason": "self_approval_blocked_for_sensitive_action", "live_trading_enabled": False}
    return {"status": "ok", "reason": "separation_of_duties_satisfied", "live_trading_enabled": False}

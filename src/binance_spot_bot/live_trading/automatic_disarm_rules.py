from __future__ import annotations

from .safety import LiveSafetyDecision, no_live_order

HARD_DISARM_TRIGGERS = {
    "restart_detected",
    "profile_changed",
    "config_changed",
    "key_changed",
    "kill_switch",
    "emergency_stop",
    "market_data_stale",
    "spread_too_high",
    "connectivity_lost",
    "reconciliation_mismatch",
    "unknown_order_state",
    "unexpected_open_order",
    "max_session_orders",
    "max_session_loss",
    "evidence_writer_failure",
}


def automatic_disarm_rules(findings: list[str]):
    return {**LiveSafetyDecision("disarm" if findings else "ok", "auto_disarm", findings, requires_approval=False).to_dict(), **no_live_order()}


def evaluate_automatic_disarm(findings: list[str]) -> dict[str, object]:
    disarm = [item for item in findings if item in HARD_DISARM_TRIGGERS]
    return {"status": "disarm" if disarm else ("warn" if findings else "ok"), "disarm_required": bool(disarm), "triggers": findings, "disarm_triggers": disarm, "live_trading_enabled": False}

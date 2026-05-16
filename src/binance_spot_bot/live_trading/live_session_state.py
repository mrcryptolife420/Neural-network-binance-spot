from __future__ import annotations

ACTIVE_STATES = {"ready_to_arm", "armed", "placing_first_order", "order_submitted"}
TRANSITIONS = {
    "locked": {"evidence_required"},
    "evidence_required": {"account_verification_required"},
    "account_verification_required": {"dry_run_required"},
    "dry_run_required": {"preview_required"},
    "preview_required": {"drills_required"},
    "drills_required": {"ready_to_arm"},
    "ready_to_arm": {"armed"},
    "armed": {"placing_first_order"},
    "placing_first_order": {"order_submitted"},
    "order_submitted": {"disarmed_after_order"},
}


def transition_live_session(from_state: str, to_state: str, *, trigger: str = "") -> dict[str, object]:
    if trigger in {"restart", "profile_edit", "config_edit", "key_change"}:
        return {"status": "ok", "from_state": from_state, "to_state": "locked", "disarmed": True, "live_trading_enabled": False}
    if trigger == "kill_switch" and from_state in ACTIVE_STATES:
        return {"status": "ok", "from_state": from_state, "to_state": "emergency_stopped", "disarmed": True, "live_trading_enabled": False}
    ok = to_state in TRANSITIONS.get(from_state, set())
    return {"status": "ok" if ok else "blocked", "from_state": from_state, "to_state": to_state, "disarmed": to_state.startswith("disarmed"), "live_trading_enabled": False}

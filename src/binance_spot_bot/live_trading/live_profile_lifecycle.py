from __future__ import annotations


def live_profile_lifecycle(state: str, action: str, approved: bool):
    return {"status": "promoted" if action == "promote" and approved else "blocked" if action == "promote" else action, "state": state, "live_trading_enabled": False}


def apply_live_profile_lifecycle(state: str, action: str, *, approved: bool, blocker: bool = False) -> dict[str, object]:
    if action == "promote" and (not approved or blocker):
        return {"status": "blocked", "from_state": state, "to_state": state, "live_trading_enabled": False}
    if action == "promote":
        return {"status": "promoted", "from_state": state, "to_state": "controlled_level_2", "live_trading_enabled": False}
    if action in {"demote", "rollback", "expire", "emergency_block"}:
        return {"status": action, "from_state": state, "to_state": {"demote": "demoted", "rollback": "controlled_level_1", "expire": "expired", "emergency_block": "emergency_blocked"}[action], "live_trading_enabled": False}
    return {"status": "blocked", "from_state": state, "to_state": state, "live_trading_enabled": False}

from __future__ import annotations

from . import CONTROLLED_SESSION_CONFIRM
from .safety import LiveSafetyDecision, no_live_order

TRANSITIONS = {
    "locked": {"plan_required"},
    "plan_required": {"plan_validated"},
    "plan_validated": {"evidence_verified"},
    "evidence_verified": {"account_verified"},
    "account_verified": {"dry_run_required"},
    "dry_run_required": {"ready_to_arm"},
    "ready_to_arm": {"armed"},
    "armed": {"running"},
    "running": {"waiting_for_reconciliation", "disarming", "completed"},
    "waiting_for_reconciliation": {"running", "disarming"},
    "disarming": {"disarmed"},
}


def live_session_manager(level: int):
    return {**LiveSafetyDecision("ready", "manage_session", [f"level_{level}"]).to_dict(), **no_live_order()}


def transition_controlled_live_session(from_state: str, to_state: str, *, trigger: str = "") -> dict[str, object]:
    if trigger in {"restart", "profile_edit", "config_edit", "key_change"}:
        return {"status": "ok", "from_state": from_state, "to_state": "disarmed", "disarmed": True, "live_trading_enabled": False}
    if trigger == "kill_switch":
        return {"status": "ok", "from_state": from_state, "to_state": "emergency_stopped", "disarmed": True, "live_trading_enabled": False}
    ok = to_state in TRANSITIONS.get(from_state, set())
    return {"status": "ok" if ok else "blocked", "from_state": from_state, "to_state": to_state, "live_trading_enabled": False}


def arm_controlled_live_session(plan_report: dict, *, confirm: str) -> dict[str, object]:
    blockers = []
    if plan_report.get("status") != "ok":
        blockers.append("valid live session plan required")
    if confirm != CONTROLLED_SESSION_CONFIRM:
        blockers.append(f"confirm required: {CONTROLLED_SESSION_CONFIRM}")
    return {"status": "blocked" if blockers else "ok", "state": "armed" if not blockers else "locked", "blockers": blockers, "live_trading_enabled": False}

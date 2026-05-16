from __future__ import annotations

from typing import Any

from .bot_profile import BotProfile, BotProfileMode, validate_bot_profile


def runtime_orchestrator_status(profile: BotProfile) -> dict[str, Any]:
    validation = validate_bot_profile(profile)
    if validation.status == "blocked":
        state = "blocked"
    elif profile.mode == BotProfileMode.LIVE_LOCKED.value:
        state = "live_training_required"
    elif profile.mode == BotProfileMode.LIVE_ARMED.value:
        state = "live_armed"
    else:
        state = "ready_to_start" if profile.auto_start_runtime else "idle"
    return {"status": "ok" if state != "blocked" else "blocked", "state": state, "validation": validation.__dict__, "live_trading_enabled": False}

def start_profile(profile: BotProfile) -> dict[str, Any]:
    status = runtime_orchestrator_status(profile)
    if profile.mode.startswith("live"):
        return {"status": "blocked", "state": "live_locked", "blockers": ["live cannot start from app-control start"], "live_trading_enabled": False}
    if status["status"] == "blocked":
        return status
    return {"status": "ok", "state": "running", "profile_id": profile.profile_id, "live_trading_enabled": False}


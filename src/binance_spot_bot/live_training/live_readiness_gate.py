from __future__ import annotations

from typing import Any

from binance_spot_bot.app_control.bot_profile import BotProfile, validate_bot_profile


def evaluate_live_readiness_gate(profile: BotProfile, validation_gate: dict[str, Any]) -> dict[str, Any]:
    profile_validation = validate_bot_profile(profile)
    blockers = list(profile_validation.blockers)
    if profile.mode != "live_locked":
        blockers.append("live readiness requires live_locked profile")
    if validation_gate.get("status") != "ok":
        blockers.append("model validation gate not passed")
    return {"status": "ready_to_arm" if not blockers else "blocked", "blockers": blockers, "manual_arm_required": True, "live_execution_implemented": False, "live_trading_enabled": False}


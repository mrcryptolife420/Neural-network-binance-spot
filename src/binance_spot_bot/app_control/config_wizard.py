from __future__ import annotations

from dataclasses import replace
from typing import Any

from .bot_profile import BotProfileMode, built_in_profiles, validate_bot_profile, bot_profile_to_dict


def create_profile_from_wizard(profile_type: str = "paper", symbol: str = "BTCUSDT") -> dict[str, Any]:
    templates = {profile.mode: profile for profile in built_in_profiles()}
    mode = {
        "backtest": BotProfileMode.BACKTEST.value,
        "paper": BotProfileMode.PAPER.value,
        "demo_spot": BotProfileMode.DEMO_SPOT.value,
        "testnet": BotProfileMode.TESTNET.value,
        "live_locked": BotProfileMode.LIVE_LOCKED.value,
    }.get(profile_type, BotProfileMode.PAPER.value)
    profile = replace(templates[mode], profile_id=f"{mode}-{symbol.lower()}-wizard", symbol=symbol)
    validation = validate_bot_profile(profile)
    return {"status": validation.status, "profile": bot_profile_to_dict(profile), "validation": validation.__dict__, "live_trading_enabled": False}


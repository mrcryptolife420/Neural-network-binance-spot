from __future__ import annotations

from .bot_profile import BotProfile


def data_bootstrap_report(profile: BotProfile) -> dict[str, object]:
    return {
        "status": "ok",
        "profile_id": profile.profile_id,
        "symbol": profile.symbol,
        "exchange_info": "fixture",
        "initial_klines": 120,
        "top_of_book": "fixture",
        "data_freshness": "ok",
        "spread_status": "ok",
        "live_order_action": False,
        "live_trading_enabled": False,
    }


from __future__ import annotations

from binance_spot_bot.ui.page_context import PageContext


def page_key() -> str:
    return "demo_spot_trading"


def validate_context(context: PageContext) -> None:
    if context.live_trading_enabled:
        raise ValueError("Demo Spot page must remain live-disabled")

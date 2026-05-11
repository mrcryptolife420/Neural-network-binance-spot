from __future__ import annotations

from binance_spot_bot.ui.page_context import PageContext


def page_key() -> str:
    return "overview"


def validate_context(context: PageContext) -> None:
    if context.live_trading_enabled:
        raise ValueError("Dashboard pages cannot enable live trading")

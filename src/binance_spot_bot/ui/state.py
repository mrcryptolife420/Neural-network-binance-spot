from __future__ import annotations

from dataclasses import replace
from decimal import Decimal

from binance_spot_bot.config import BotSettings
from binance_spot_bot.runtime import BotRuntime, DATA_SOURCES, RuntimeOptions, UI_MODES

SELECTABLE_MODES = UI_MODES
SELECTABLE_DATA_SOURCES = DATA_SOURCES


def create_runtime(
    settings: BotSettings,
    mode: str,
    symbol: str,
    interval: str,
    scenario: str,
    seed: int,
    max_daily_loss_quote: Decimal,
    max_position_quote: Decimal,
    max_trades_per_day: int,
    min_signal_confidence: float,
    max_spread_bps: Decimal,
    source: str = "auto",
    model_alias: str = "",
    max_data_age_ms: int = 120_000,
    default_quote_size: Decimal = Decimal("10"),
    demo_trading_armed: bool = False,
    max_demo_orders_per_session: int = 25,
    demo_pilot_preset: str = "smoke",
) -> BotRuntime:
    safe_settings = replace(settings, live_trading_enabled=False)
    return BotRuntime(
        safe_settings,
        RuntimeOptions(
            mode=mode,
            symbol=symbol,
            interval=interval,
            scenario=scenario,
            seed=seed,
            source=source,
            model_alias=model_alias,
            max_daily_loss_quote=max_daily_loss_quote,
            max_position_quote=max_position_quote,
            max_trades_per_day=max_trades_per_day,
            min_signal_confidence=min_signal_confidence,
            max_spread_bps=max_spread_bps,
            max_data_age_ms=max_data_age_ms,
            default_quote_size=default_quote_size,
            demo_trading_armed=demo_trading_armed,
            max_demo_orders_per_session=max_demo_orders_per_session,
            demo_pilot_preset=demo_pilot_preset,
        ),
    )

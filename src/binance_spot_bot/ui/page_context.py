from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from binance_spot_bot.config import BotSettings


@dataclass(frozen=True)
class PageContext:
    settings: BotSettings
    runtime: Any
    snapshot: Any
    profile: Any
    symbol: str
    interval: str
    source: str
    live_trading_enabled: bool = False

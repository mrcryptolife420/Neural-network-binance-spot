from __future__ import annotations

import time
from dataclasses import dataclass
from decimal import Decimal

from .portfolio import Portfolio


@dataclass(frozen=True)
class PortfolioRiskLimits:
    max_total_exposure: Decimal
    max_open_positions: int
    max_daily_loss: Decimal
    per_symbol_cooldown_ms: int = 60_000


class PortfolioRiskEngine:
    def __init__(self, limits: PortfolioRiskLimits):
        self.limits = limits
        self.last_trade_ms: dict[str, int] = {}

    def can_enter(self, portfolio: Portfolio, symbol: str, marks: dict[str, Decimal], daily_pnl: Decimal = Decimal("0")) -> tuple[bool, str]:
        if daily_pnl <= -self.limits.max_daily_loss:
            return False, "global daily loss limit reached"
        if portfolio.total_exposure(marks) >= self.limits.max_total_exposure:
            return False, "portfolio exposure limit reached"
        open_positions = sum(1 for position in portfolio.positions.values() if position.quantity > 0)
        if symbol not in portfolio.positions and open_positions >= self.limits.max_open_positions:
            return False, "max open positions reached"
        now_ms = int(time.time() * 1000)
        if now_ms - self.last_trade_ms.get(symbol, 0) < self.limits.per_symbol_cooldown_ms:
            return False, "symbol cooldown active"
        return True, "portfolio risk checks passed"

    def record_trade(self, symbol: str) -> None:
        self.last_trade_ms[symbol] = int(time.time() * 1000)

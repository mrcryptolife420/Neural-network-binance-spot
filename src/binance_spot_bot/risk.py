from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .types import (
    AccountState,
    MarketState,
    OrderSide,
    OrderType,
    RiskDecision,
    RiskDecisionType,
    Signal,
    SignalSide,
    TradeIntent,
)


@dataclass(frozen=True)
class RiskLimits:
    max_daily_loss_quote: Decimal
    max_position_quote: Decimal
    max_trades_per_day: int
    min_signal_confidence: float
    max_spread_bps: Decimal
    max_data_age_ms: int = 120_000
    default_quote_size: Decimal = Decimal("10")
    max_slippage_bps: Decimal = Decimal("10")


class RiskEngine:
    def __init__(self, limits: RiskLimits, kill_switch: bool = True):
        self.limits = limits
        self.kill_switch = kill_switch
        self.trades_today = 0

    def decide(self, signal: Signal, account: AccountState, market: MarketState) -> RiskDecision:
        if self.kill_switch:
            return self._block("kill switch active")
        if signal.signal == SignalSide.HOLD:
            return self._block("model returned HOLD")
        if signal.confidence < self.limits.min_signal_confidence:
            return self._block("signal confidence below threshold")
        if self.limits.max_trades_per_day <= 0:
            return self._block("max trades per day is zero")
        if self.trades_today >= self.limits.max_trades_per_day:
            return self._block("max trades per day reached")
        if self.limits.max_position_quote <= 0:
            return self._block("max position quote is zero")
        if account.daily_realized_pnl <= -self.limits.max_daily_loss_quote:
            return self._block("daily max loss reached")
        if market.now_ms is not None and market.data_timestamp_ms is not None:
            if market.now_ms - market.data_timestamp_ms > self.limits.max_data_age_ms:
                return self._block("market data is stale")
        spread = market.spread_bps
        if spread is not None and spread > self.limits.max_spread_bps:
            return self._block("spread above threshold")

        quote_size = min(self.limits.default_quote_size, self.limits.max_position_quote)
        if quote_size <= 0:
            return self._block("quote size is zero")
        if signal.signal == SignalSide.BUY and account.quote_balance < quote_size:
            return self._block("insufficient quote balance")
        side = OrderSide.BUY if signal.signal == SignalSide.BUY else OrderSide.SELL
        intent = TradeIntent(
            symbol=market.symbol,
            side=side,
            quote_size=quote_size,
            order_type=OrderType.MARKET,
            max_slippage_bps=self.limits.max_slippage_bps,
        )
        return RiskDecision(RiskDecisionType.ALLOW, "risk checks passed", intent)

    def record_trade(self) -> None:
        self.trades_today += 1

    @staticmethod
    def _block(reason: str) -> RiskDecision:
        return RiskDecision(RiskDecisionType.BLOCK, reason, None)


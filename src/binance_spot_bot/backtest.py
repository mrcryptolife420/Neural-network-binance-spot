from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .risk import RiskEngine
from .signal_model import RuleBasedSignalModel, TinyNeuralSignalModel
from .types import AccountState, FeatureRow, MarketState, RiskDecisionType, SignalSide


@dataclass(frozen=True)
class BacktestResult:
    trades: int
    blocked: int
    final_equity: Decimal
    pnl: Decimal
    max_drawdown: Decimal


class BacktestEngine:
    def __init__(
        self,
        risk_engine: RiskEngine,
        fee_bps: Decimal = Decimal("10"),
        slippage_bps: Decimal = Decimal("5"),
    ):
        self.risk_engine = risk_engine
        self.fee_bps = fee_bps
        self.slippage_bps = slippage_bps

    def run(
        self,
        rows: list[FeatureRow],
        model: RuleBasedSignalModel | TinyNeuralSignalModel,
        starting_quote: Decimal = Decimal("1000"),
    ) -> BacktestResult:
        quote = starting_quote
        base = Decimal("0")
        peak = starting_quote
        max_drawdown = Decimal("0")
        trades = 0
        blocked = 0
        for row in rows:
            price = row.close
            equity = quote + (base * price)
            peak = max(peak, equity)
            drawdown = peak - equity
            max_drawdown = max(max_drawdown, drawdown)
            signal = model.predict(row)
            account = AccountState(quote_balance=quote, base_balance=base, equity_quote=equity)
            market = MarketState(row.symbol, price, data_timestamp_ms=row.timestamp_ms, now_ms=row.timestamp_ms)
            decision = self.risk_engine.decide(signal, account, market)
            if decision.decision != RiskDecisionType.ALLOW or decision.intent is None:
                blocked += 1
                continue
            fee_multiplier = Decimal("1") - (self.fee_bps / Decimal("10000"))
            slip_multiplier = Decimal("1") + (self.slippage_bps / Decimal("10000"))
            if signal.signal == SignalSide.BUY:
                spend = min(decision.intent.quote_size, quote)
                qty = (spend / (price * slip_multiplier)) * fee_multiplier
                quote -= spend
                base += qty
            elif signal.signal == SignalSide.SELL and base > 0:
                receive = (base * price / slip_multiplier) * fee_multiplier
                quote += receive
                base = Decimal("0")
            self.risk_engine.record_trade()
            trades += 1
        final_equity = quote + (base * rows[-1].close if rows else Decimal("0"))
        return BacktestResult(trades, blocked, final_equity, final_equity - starting_quote, max_drawdown)


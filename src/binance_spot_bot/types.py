from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Any


class TradingMode(str, Enum):
    DISABLED = "disabled"
    PAPER = "paper"
    TESTNET = "testnet"
    LIVE = "live"


class SignalSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class RiskDecisionType(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


@dataclass(frozen=True)
class Candle:
    open_time_ms: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    close_time_ms: int
    quote_volume: Decimal = Decimal("0")
    trade_count: int = 0


@dataclass(frozen=True)
class SymbolFilters:
    symbol: str
    status: str
    tick_size: Decimal
    step_size: Decimal
    min_qty: Decimal
    max_qty: Decimal
    min_notional: Decimal
    market_max_qty: Decimal | None = None


@dataclass(frozen=True)
class FeatureRow:
    symbol: str
    timestamp_ms: int
    values: dict[str, float]
    close: Decimal


@dataclass(frozen=True)
class LabelRow:
    timestamp_ms: int
    horizon_bars: int
    future_return: float
    label: int


@dataclass(frozen=True)
class Signal:
    signal: SignalSide
    confidence: float
    horizon: str
    model_version: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AccountState:
    quote_balance: Decimal
    base_balance: Decimal = Decimal("0")
    equity_quote: Decimal | None = None
    daily_realized_pnl: Decimal = Decimal("0")
    open_order_count: int = 0


@dataclass(frozen=True)
class MarketState:
    symbol: str
    last_price: Decimal
    bid: Decimal | None = None
    ask: Decimal | None = None
    data_timestamp_ms: int | None = None
    now_ms: int | None = None

    @property
    def spread_bps(self) -> Decimal | None:
        if self.bid is None or self.ask is None or self.bid <= 0:
            return None
        mid = (self.bid + self.ask) / Decimal("2")
        if mid <= 0:
            return None
        return ((self.ask - self.bid) / mid) * Decimal("10000")


@dataclass(frozen=True)
class TradeIntent:
    symbol: str
    side: OrderSide
    quote_size: Decimal
    order_type: OrderType
    max_slippage_bps: Decimal


@dataclass(frozen=True)
class RiskDecision:
    decision: RiskDecisionType
    reason: str
    intent: TradeIntent | None = None


@dataclass(frozen=True)
class OrderRequest:
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: Decimal | None = None
    quote_order_qty: Decimal | None = None
    price: Decimal | None = None
    client_order_id: str | None = None


@dataclass(frozen=True)
class ExecutionResult:
    mode: TradingMode
    status: str
    order_request: OrderRequest | None
    response: dict[str, Any]


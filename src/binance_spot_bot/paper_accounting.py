from __future__ import annotations

from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Any

from .types import OrderSide


@dataclass(frozen=True)
class PaperFill:
    symbol: str
    side: OrderSide
    quantity: Decimal
    price: Decimal
    notional: Decimal
    fee: Decimal
    realized_pnl: Decimal

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["side"] = self.side.value
        return {key: str(value) if isinstance(value, Decimal) else value for key, value in payload.items()}


@dataclass
class PaperAccount:
    quote_balance: Decimal
    base_balance: Decimal = Decimal("0")
    average_entry: Decimal = Decimal("0")
    realized_pnl: Decimal = Decimal("0")
    fee_bps: Decimal = Decimal("10")
    slippage_bps: Decimal = Decimal("0")
    fills: list[PaperFill] = field(default_factory=list)

    def buy(self, symbol: str, quantity: Decimal, price: Decimal) -> PaperFill:
        price = self._buy_price(price)
        notional = quantity * price
        fee = notional * self.fee_bps / Decimal("10000")
        if self.quote_balance < notional + fee:
            raise ValueError("insufficient quote balance")
        previous_cost = self.average_entry * self.base_balance
        self.quote_balance -= notional + fee
        self.base_balance += quantity
        self.average_entry = (previous_cost + notional) / self.base_balance if self.base_balance else Decimal("0")
        return self._record(symbol, OrderSide.BUY, quantity, price, notional, fee, Decimal("0"))

    def sell(self, symbol: str, quantity: Decimal, price: Decimal) -> PaperFill:
        if self.base_balance < quantity:
            raise ValueError("insufficient base balance")
        price = self._sell_price(price)
        notional = quantity * price
        fee = notional * self.fee_bps / Decimal("10000")
        pnl = (price - self.average_entry) * quantity - fee
        self.quote_balance += notional - fee
        self.base_balance -= quantity
        self.realized_pnl += pnl
        if self.base_balance == 0:
            self.average_entry = Decimal("0")
        return self._record(symbol, OrderSide.SELL, quantity, price, notional, fee, pnl)

    def equity(self, mark_price: Decimal) -> Decimal:
        return self.quote_balance + (self.base_balance * mark_price)

    def to_dict(self, mark_price: Decimal | None = None) -> dict[str, Any]:
        payload = {
            "quote_balance": self.quote_balance,
            "base_balance": self.base_balance,
            "average_entry": self.average_entry,
            "realized_pnl": self.realized_pnl,
            "fees_paid": sum((fill.fee for fill in self.fills), Decimal("0")),
            "slippage_bps": self.slippage_bps,
            "fills": [fill.to_dict() for fill in self.fills],
        }
        if mark_price is not None:
            payload["equity"] = self.equity(mark_price)
        return {key: str(value) if isinstance(value, Decimal) else value for key, value in payload.items()}

    def _record(self, symbol: str, side: OrderSide, quantity: Decimal, price: Decimal, notional: Decimal, fee: Decimal, pnl: Decimal) -> PaperFill:
        fill = PaperFill(symbol, side, quantity, price, notional, fee, pnl)
        self.fills.append(fill)
        return fill

    def _buy_price(self, price: Decimal) -> Decimal:
        return price * (Decimal("1") + self.slippage_bps / Decimal("10000"))

    def _sell_price(self, price: Decimal) -> Decimal:
        return price / (Decimal("1") + self.slippage_bps / Decimal("10000"))

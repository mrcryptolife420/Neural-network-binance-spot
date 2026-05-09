from __future__ import annotations

from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Any


@dataclass
class Position:
    symbol: str
    quantity: Decimal = Decimal("0")
    average_entry: Decimal = Decimal("0")

    def value(self, mark_price: Decimal) -> Decimal:
        return self.quantity * mark_price


@dataclass
class Portfolio:
    balances: dict[str, Decimal] = field(default_factory=lambda: {"USDT": Decimal("0")})
    positions: dict[str, Position] = field(default_factory=dict)
    fees_paid: Decimal = Decimal("0")
    realized_pnl: Decimal = Decimal("0")

    def set_balance(self, asset: str, amount: Decimal) -> None:
        self.balances[asset] = amount

    def buy(self, symbol: str, quote_asset: str, quote_size: Decimal, price: Decimal, fee_bps: Decimal = Decimal("10"), slippage_bps: Decimal = Decimal("0")) -> None:
        fill_price = price * (Decimal("1") + slippage_bps / Decimal("10000"))
        fee = quote_size * fee_bps / Decimal("10000")
        if self.balances.get(quote_asset, Decimal("0")) < quote_size + fee:
            raise ValueError("insufficient portfolio quote balance")
        qty = quote_size / fill_price
        self.balances[quote_asset] -= quote_size + fee
        self.fees_paid += fee
        position = self.positions.setdefault(symbol, Position(symbol))
        previous_cost = position.quantity * position.average_entry
        position.quantity += qty
        position.average_entry = (previous_cost + quote_size) / position.quantity

    def sell(self, symbol: str, quote_asset: str, quantity: Decimal, price: Decimal, fee_bps: Decimal = Decimal("10"), slippage_bps: Decimal = Decimal("0")) -> None:
        position = self.positions.setdefault(symbol, Position(symbol))
        if position.quantity < quantity:
            raise ValueError("insufficient portfolio base balance")
        fill_price = price / (Decimal("1") + slippage_bps / Decimal("10000"))
        notional = quantity * fill_price
        fee = notional * fee_bps / Decimal("10000")
        position.quantity -= quantity
        self.balances[quote_asset] = self.balances.get(quote_asset, Decimal("0")) + notional - fee
        self.realized_pnl += (fill_price - position.average_entry) * quantity - fee
        self.fees_paid += fee
        if position.quantity == 0:
            position.average_entry = Decimal("0")

    def total_equity(self, marks: dict[str, Decimal], quote_asset: str = "USDT") -> Decimal:
        equity = self.balances.get(quote_asset, Decimal("0"))
        for symbol, position in self.positions.items():
            equity += position.value(marks.get(symbol, Decimal("0")))
        return equity

    def total_exposure(self, marks: dict[str, Decimal]) -> Decimal:
        return sum((position.value(marks.get(symbol, Decimal("0"))) for symbol, position in self.positions.items()), Decimal("0"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "balances": {key: str(value) for key, value in self.balances.items()},
            "positions": {key: {k: str(v) if isinstance(v, Decimal) else v for k, v in asdict(value).items()} for key, value in self.positions.items()},
            "fees_paid": str(self.fees_paid),
            "realized_pnl": str(self.realized_pnl),
        }

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .types import TradeIntent


@dataclass(frozen=True)
class ShadowOrder:
    symbol: str
    side: str
    quote_size: str
    reason: str = "would-be order only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ShadowMode:
    def __init__(self) -> None:
        self.orders: list[ShadowOrder] = []
        self.market_data: list[dict[str, Any]] = []

    def record_market_data(self, payload: dict[str, Any]) -> None:
        self.market_data.append(dict(payload))

    def record_intent(self, intent: TradeIntent) -> ShadowOrder:
        order = ShadowOrder(intent.symbol, intent.side.value, str(intent.quote_size))
        self.orders.append(order)
        return order

    def place_order(self, *args: Any, **kwargs: Any) -> None:
        raise RuntimeError("shadow mode cannot place signed orders")

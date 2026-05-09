from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any

from .market_stream import BookTickerEvent
from .types import MarketState


@dataclass(frozen=True)
class TopOfBook:
    symbol: str
    bid: Decimal
    bid_qty: Decimal
    ask: Decimal
    ask_qty: Decimal
    event_time_ms: int | None
    last_update_id: int
    received_time_ms: int

    @property
    def mid_price(self) -> Decimal | None:
        if self.bid <= 0 or self.ask <= 0:
            return None
        return (self.bid + self.ask) / Decimal("2")

    @property
    def spread_bps(self) -> Decimal | None:
        mid = self.mid_price
        if mid is None or mid <= 0:
            return None
        return ((self.ask - self.bid) / mid) * Decimal("10000")

    def age_ms(self, now_ms: int) -> int:
        timestamp = self.event_time_ms or self.received_time_ms
        return max(0, now_ms - timestamp)

    def to_dict(self, now_ms: int | None = None) -> dict[str, Any]:
        payload = {k: str(v) if isinstance(v, Decimal) else v for k, v in asdict(self).items()}
        payload["mid_price"] = str(self.mid_price) if self.mid_price is not None else None
        payload["spread_bps"] = str(self.spread_bps) if self.spread_bps is not None else None
        if now_ms is not None:
            payload["age_ms"] = self.age_ms(now_ms)
        return payload


class TopOfBookFeed:
    def __init__(self) -> None:
        self.current: TopOfBook | None = None

    def update(self, event: BookTickerEvent, received_time_ms: int) -> TopOfBook:
        self.current = TopOfBook(
            symbol=event.symbol,
            bid=event.bid,
            bid_qty=event.bid_qty,
            ask=event.ask,
            ask_qty=event.ask_qty,
            event_time_ms=event.event_time_ms,
            last_update_id=event.update_id,
            received_time_ms=received_time_ms,
        )
        return self.current

    def market_state(
        self,
        symbol: str,
        last_price: Decimal,
        now_ms: int,
        fallback_timestamp_ms: int | None = None,
    ) -> MarketState:
        if self.current and self.current.symbol == symbol:
            timestamp = self.current.event_time_ms or self.current.received_time_ms
            return MarketState(
                symbol=symbol,
                last_price=last_price,
                bid=self.current.bid,
                ask=self.current.ask,
                data_timestamp_ms=timestamp,
                now_ms=now_ms,
            )
        return MarketState(
            symbol=symbol,
            last_price=last_price,
            bid=None,
            ask=None,
            data_timestamp_ms=fallback_timestamp_ms,
            now_ms=now_ms,
        )

    def snapshot(self, now_ms: int | None = None) -> dict[str, Any]:
        if self.current is None:
            return {"status": "empty"}
        payload = self.current.to_dict(now_ms)
        payload["status"] = "ok"
        return payload


@dataclass
class DepthBookBuilder:
    last_update_id: int | None = None
    resync_required: bool = False

    def apply_snapshot(self, last_update_id: int) -> None:
        self.last_update_id = last_update_id
        self.resync_required = False

    def apply_diff(self, first_update_id: int, final_update_id: int, previous_final_update_id: int | None = None) -> bool:
        if self.resync_required:
            return False
        if self.last_update_id is None:
            self.resync_required = True
            return False
        expected_previous = self.last_update_id if previous_final_update_id is None else previous_final_update_id
        if final_update_id <= self.last_update_id:
            return False
        if first_update_id > expected_previous + 1:
            self.resync_required = True
            return False
        self.last_update_id = final_update_id
        return True

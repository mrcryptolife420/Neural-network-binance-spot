from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


BINANCE_STREAM_BASE_URL = "wss://stream.binance.com:9443"
MAX_STREAM_CONNECTION_AGE_MS = 23 * 60 * 60 * 1000


@dataclass(frozen=True)
class KlineStreamEvent:
    symbol: str
    interval: str
    event_time_ms: int
    open_time_ms: int
    close_time_ms: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    is_closed: bool
    trade_count: int


@dataclass(frozen=True)
class BookTickerEvent:
    symbol: str
    update_id: int
    bid: Decimal
    bid_qty: Decimal
    ask: Decimal
    ask_qty: Decimal
    event_time_ms: int | None = None


@dataclass(frozen=True)
class TradeStreamEvent:
    symbol: str
    trade_id: int
    price: Decimal
    quantity: Decimal
    event_time_ms: int
    trade_time_ms: int


@dataclass(frozen=True)
class MiniTickerEvent:
    symbol: str
    event_time_ms: int
    close: Decimal
    open: Decimal
    high: Decimal
    low: Decimal
    volume: Decimal
    quote_volume: Decimal


@dataclass(frozen=True)
class StreamStatus:
    connected: bool
    status: str
    message: str
    last_event_time_ms: int | None = None
    reconnect_count: int = 0


@dataclass(frozen=True)
class ReconnectDecision:
    should_reconnect: bool
    delay_seconds: float
    reason: str


@dataclass
class ReconnectPolicy:
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 30.0
    max_connection_age_ms: int = MAX_STREAM_CONNECTION_AGE_MS
    attempts: int = 0

    def next_delay(self) -> float:
        delay = min(self.max_delay_seconds, self.base_delay_seconds * (2**self.attempts))
        self.attempts += 1
        return delay

    def reset(self) -> None:
        self.attempts = 0

    def evaluate(
        self,
        *,
        connected: bool,
        connection_started_ms: int | None,
        now_ms: int,
        last_error: str | None = None,
    ) -> ReconnectDecision:
        if last_error:
            return ReconnectDecision(True, self.next_delay(), last_error)
        if not connected:
            return ReconnectDecision(True, self.next_delay(), "stream disconnected")
        if connection_started_ms is not None:
            if now_ms - connection_started_ms >= self.max_connection_age_ms:
                return ReconnectDecision(True, 0.0, "scheduled reconnect before 24h limit")
        return ReconnectDecision(False, 0.0, "connection healthy")


def normalize_stream_symbol(symbol: str) -> str:
    normalized = symbol.strip().lower()
    if not normalized or not normalized.replace("_", "").isalnum():
        raise ValueError("symbol must be alphanumeric")
    return normalized


def stream_name(symbol: str, kind: str, interval: str | None = None) -> str:
    normalized = normalize_stream_symbol(symbol)
    if kind == "kline":
        if not interval:
            raise ValueError("interval is required for kline streams")
        return f"{normalized}@kline_{interval}"
    if kind in {"bookTicker", "trade", "miniTicker"}:
        return f"{normalized}@{kind}"
    raise ValueError(f"unsupported stream kind: {kind}")


def combined_stream_url(streams: list[str], base_url: str = BINANCE_STREAM_BASE_URL) -> str:
    if not streams:
        raise ValueError("at least one stream is required")
    return f"{base_url.rstrip('/')}/stream?streams={'/'.join(streams)}"


def subscribe_payload(streams: list[str], request_id: int = 1) -> dict[str, Any]:
    if not streams:
        raise ValueError("at least one stream is required")
    return {"method": "SUBSCRIBE", "params": streams, "id": request_id}


def unsubscribe_payload(streams: list[str], request_id: int = 1) -> dict[str, Any]:
    if not streams:
        raise ValueError("at least one stream is required")
    return {"method": "UNSUBSCRIBE", "params": streams, "id": request_id}


def parse_stream_message(payload: str | bytes | dict[str, Any]) -> Any:
    if isinstance(payload, (str, bytes)):
        payload = json.loads(payload)
    data = payload.get("data", payload)
    event_type = data.get("e")
    if event_type == "kline":
        return parse_kline_event(data)
    if event_type == "trade":
        return parse_trade_event(data)
    if event_type == "24hrMiniTicker":
        return parse_mini_ticker_event(data)
    if "b" in data and "a" in data and "u" in data:
        return parse_book_ticker_event(data)
    raise ValueError(f"unsupported stream payload: {event_type or sorted(data.keys())}")


def parse_kline_event(data: dict[str, Any]) -> KlineStreamEvent:
    kline = data["k"]
    return KlineStreamEvent(
        symbol=str(data.get("s", kline["s"])).upper(),
        interval=str(kline["i"]),
        event_time_ms=int(data["E"]),
        open_time_ms=int(kline["t"]),
        close_time_ms=int(kline["T"]),
        open=Decimal(str(kline["o"])),
        high=Decimal(str(kline["h"])),
        low=Decimal(str(kline["l"])),
        close=Decimal(str(kline["c"])),
        volume=Decimal(str(kline["v"])),
        is_closed=bool(kline["x"]),
        trade_count=int(kline["n"]),
    )


def parse_book_ticker_event(data: dict[str, Any]) -> BookTickerEvent:
    return BookTickerEvent(
        symbol=str(data["s"]).upper(),
        update_id=int(data["u"]),
        bid=Decimal(str(data["b"])),
        bid_qty=Decimal(str(data["B"])),
        ask=Decimal(str(data["a"])),
        ask_qty=Decimal(str(data["A"])),
        event_time_ms=int(data["E"]) if "E" in data else None,
    )


def parse_trade_event(data: dict[str, Any]) -> TradeStreamEvent:
    return TradeStreamEvent(
        symbol=str(data["s"]).upper(),
        trade_id=int(data["t"]),
        price=Decimal(str(data["p"])),
        quantity=Decimal(str(data["q"])),
        event_time_ms=int(data["E"]),
        trade_time_ms=int(data["T"]),
    )


def parse_mini_ticker_event(data: dict[str, Any]) -> MiniTickerEvent:
    return MiniTickerEvent(
        symbol=str(data["s"]).upper(),
        event_time_ms=int(data["E"]),
        close=Decimal(str(data["c"])),
        open=Decimal(str(data["o"])),
        high=Decimal(str(data["h"])),
        low=Decimal(str(data["l"])),
        volume=Decimal(str(data["v"])),
        quote_volume=Decimal(str(data["q"])),
    )

from __future__ import annotations

import time
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Protocol

from .binance import BinanceAPIError, BinanceSpotAdapter
from .config import BotSettings
from .data import DataStore, parse_binance_klines
from .demo import DemoMarketReplay
from .market_stream import StreamStatus, combined_stream_url, stream_name
from .orderbook import TopOfBook
from .types import Candle


@dataclass(frozen=True)
class MarketDataSnapshot:
    candles: list[Candle]
    top_of_book: TopOfBook | None
    source: str
    status: str
    message: str
    last_event_age_ms: int | None = None
    reconnect_count: int = 0
    stream_url: str | None = None


class MarketDataSource(Protocol):
    def next_event(self) -> Candle | None:
        ...

    def snapshot(self) -> MarketDataSnapshot:
        ...

    def status(self) -> StreamStatus:
        ...

    def close(self) -> None:
        ...


class StaticMarketDataSource:
    def __init__(self, symbol: str, candles: list[Candle], source: str = "static"):
        self.symbol = symbol
        self._candles = candles
        self._index = 0
        self._closed = False
        self._source = source

    def next_event(self) -> Candle | None:
        if self._closed or self._index >= len(self._candles):
            return None
        candle = self._candles[self._index]
        self._index += 1
        return candle

    def snapshot(self) -> MarketDataSnapshot:
        return MarketDataSnapshot(
            candles=self._candles[: self._index],
            top_of_book=_synthetic_book(self.symbol, self._candles[self._index - 1]) if self._index else None,
            source=self._source,
            status="completed" if self._index >= len(self._candles) else "ok",
            message=f"{self._source} source",
            last_event_age_ms=0 if self._index else None,
        )

    def status(self) -> StreamStatus:
        return StreamStatus(not self._closed, "ok", f"{self._source} source")

    def close(self) -> None:
        self._closed = True


@dataclass
class DemoMarketReplaySource:
    symbol: str
    interval: str = "1m"
    scenario: str = "sideways"
    seed: int = 7
    count: int = 240
    _candles: list[Candle] = field(init=False)
    _index: int = field(default=0, init=False)
    _closed: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        self._candles = DemoMarketReplay(
            symbol=self.symbol,
            scenario=self.scenario,
            seed=self.seed,
            count=self.count,
        ).candles()

    def next_event(self) -> Candle | None:
        if self._closed or self._index >= len(self._candles):
            return None
        candle = self._candles[self._index]
        self._index += 1
        return candle

    def snapshot(self) -> MarketDataSnapshot:
        return MarketDataSnapshot(
            candles=self._candles[: self._index],
            top_of_book=_synthetic_book(self.symbol, self._candles[self._index - 1]) if self._index else None,
            source="demo",
            status="completed" if self._index >= len(self._candles) else "ok",
            message="demo replay source",
            last_event_age_ms=0 if self._index else None,
        )

    def status(self) -> StreamStatus:
        return StreamStatus(not self._closed, "ok", "demo replay source")

    def close(self) -> None:
        self._closed = True


class RestPollingMarketDataSource:
    def __init__(
        self,
        settings: BotSettings,
        symbol: str,
        interval: str,
        datastore: DataStore,
        limit: int = 120,
        fallback: DemoMarketReplaySource | None = None,
    ):
        self.settings = settings
        self.symbol = symbol
        self.interval = interval
        self.datastore = datastore
        self.limit = limit
        self.fallback = fallback
        self._candles: list[Candle] = []
        self._index = 0
        self._status = "created"
        self._message = "not fetched"
        self._closed = False
        self._fetch_once()

    def _fetch_once(self) -> None:
        try:
            raw = BinanceSpotAdapter(self.settings).get_klines(self.symbol, self.interval, limit=self.limit)
            self._candles = parse_binance_klines(raw)
            self.datastore.save_raw_json(f"{self.symbol}_{self.interval}_latest", raw)
            self.datastore.save_candles_csv(self.symbol, self.interval, self._candles)
            self._status = "ok"
            self._message = "rest polling source"
        except (BinanceAPIError, OSError, ValueError) as exc:
            self._status = "degraded"
            self._message = f"REST fetch failed; using fallback data: {exc}"
            if self.fallback is None:
                self.fallback = DemoMarketReplaySource(self.symbol, self.interval, count=max(self.limit, 80))

    def next_event(self) -> Candle | None:
        if self._closed:
            return None
        if self.fallback and not self._candles:
            return self.fallback.next_event()
        if self._index >= len(self._candles):
            return None
        candle = self._candles[self._index]
        self._index += 1
        return candle

    def snapshot(self) -> MarketDataSnapshot:
        if self.fallback and not self._candles:
            snap = self.fallback.snapshot()
            return MarketDataSnapshot(
                candles=snap.candles,
                top_of_book=snap.top_of_book,
                source="rest",
                status=self._status,
                message=self._message,
                last_event_age_ms=snap.last_event_age_ms,
            )
        return MarketDataSnapshot(
            candles=self._candles[: self._index],
            top_of_book=_synthetic_book(self.symbol, self._candles[self._index - 1]) if self._index else None,
            source="rest",
            status=self._status,
            message=self._message,
            last_event_age_ms=0 if self._index else None,
        )

    def status(self) -> StreamStatus:
        return StreamStatus(not self._closed, self._status, self._message)

    def close(self) -> None:
        self._closed = True
        if self.fallback:
            self.fallback.close()


class WebSocketMarketDataSource:
    def __init__(
        self,
        settings: BotSettings,
        symbol: str,
        interval: str,
        datastore: DataStore,
        limit: int = 120,
    ):
        self.symbol = symbol
        self.interval = interval
        self.reconnect_count = 0
        streams = [stream_name(symbol, "kline", interval), stream_name(symbol, "bookTicker")]
        self.stream_url = combined_stream_url(streams)
        self.fallback = RestPollingMarketDataSource(
            settings,
            symbol,
            interval,
            datastore,
            limit=limit,
            fallback=DemoMarketReplaySource(symbol, interval, count=max(limit, 80)),
        )
        self._message = "websocket adapter is market-data-only; local runtime uses safe polling fallback until async loop is enabled"

    def next_event(self) -> Candle | None:
        return self.fallback.next_event()

    def snapshot(self) -> MarketDataSnapshot:
        snap = self.fallback.snapshot()
        return MarketDataSnapshot(
            candles=snap.candles,
            top_of_book=snap.top_of_book,
            source="websocket",
            status="degraded",
            message=self._message,
            last_event_age_ms=snap.last_event_age_ms,
            reconnect_count=self.reconnect_count,
            stream_url=self.stream_url,
        )

    def status(self) -> StreamStatus:
        return StreamStatus(False, "degraded", self._message, reconnect_count=self.reconnect_count)

    def close(self) -> None:
        self.fallback.close()


def _synthetic_book(symbol: str, candle: Candle) -> TopOfBook:
    bid = (candle.close * Decimal("0.9999")).quantize(Decimal("0.0001"))
    ask = (candle.close * Decimal("1.0001")).quantize(Decimal("0.0001"))
    now_ms = int(time.time() * 1000)
    return TopOfBook(
        symbol=symbol,
        bid=bid,
        bid_qty=Decimal("1"),
        ask=ask,
        ask_qty=Decimal("1"),
        event_time_ms=candle.close_time_ms,
        last_update_id=candle.close_time_ms,
        received_time_ms=now_ms,
    )

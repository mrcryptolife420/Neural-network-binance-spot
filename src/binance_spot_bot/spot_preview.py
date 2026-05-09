from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any

from .binance import BinanceAPIError, BinanceSpotAdapter
from .config import BotSettings
from .data import parse_binance_klines
from .demo import DemoMarketReplay
from .types import Candle, SymbolFilters


@dataclass(frozen=True)
class SpotPreview:
    symbol: str
    status: str
    last_price: Decimal
    bid: Decimal | None
    ask: Decimal | None
    spread_bps: Decimal | None
    filters: SymbolFilters
    candles: list[Candle]
    source: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["last_price"] = str(self.last_price)
        payload["bid"] = str(self.bid) if self.bid is not None else None
        payload["ask"] = str(self.ask) if self.ask is not None else None
        payload["spread_bps"] = str(self.spread_bps) if self.spread_bps is not None else None
        return payload


def load_spot_symbol_preview(
    settings: BotSettings,
    symbol: str = "BTCUSDT",
    interval: str = "1m",
    limit: int = 60,
    adapter: BinanceSpotAdapter | None = None,
) -> SpotPreview:
    try:
        adapter = adapter or BinanceSpotAdapter(settings)
        filters = adapter.get_symbol_filters(symbol)
        order_book = adapter.get_order_book(symbol, depth=5)
        raw_klines = adapter.get_klines(symbol, interval, limit=limit)
        candles = parse_binance_klines(raw_klines)
        bid = Decimal(str(order_book["bids"][0][0])) if order_book.get("bids") else None
        ask = Decimal(str(order_book["asks"][0][0])) if order_book.get("asks") else None
        last = candles[-1].close if candles else Decimal("0")
        spread = _spread_bps(bid, ask)
        return SpotPreview(symbol, filters.status, last, bid, ask, spread, filters, candles, "public-rest", "public Binance Spot preview")
    except (BinanceAPIError, OSError, ValueError, KeyError):
        candles = DemoMarketReplay(symbol=symbol, count=max(limit, 60)).candles()
        last = candles[-1].close
        bid = last * Decimal("0.9999")
        ask = last * Decimal("1.0001")
        filters = SymbolFilters(symbol, "DEMO", Decimal("0.01"), Decimal("0.00001"), Decimal("0.00001"), Decimal("100000"), Decimal("5"))
        return SpotPreview(symbol, "DEMO", last, bid, ask, _spread_bps(bid, ask), filters, candles, "demo-fallback", "Binance unavailable; using local demo preview")


def _spread_bps(bid: Decimal | None, ask: Decimal | None) -> Decimal | None:
    if bid is None or ask is None or bid <= 0:
        return None
    mid = (bid + ask) / Decimal("2")
    if mid <= 0:
        return None
    return ((ask - bid) / mid) * Decimal("10000")

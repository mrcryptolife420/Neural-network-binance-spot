from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .binance import BinanceAPIError, BinanceSpotAdapter
from .config import BotSettings
from .data import DataStore, parse_binance_klines
from .public_data_quality import bundle_quality
from .redaction import redact_payload
from .types import Candle


PUBLIC_ENDPOINTS = {
    "exchange_info": "/api/v3/exchangeInfo",
    "klines": "/api/v3/klines",
    "ui_klines": "/api/v3/uiKlines",
    "depth": "/api/v3/depth",
    "ticker_24h": "/api/v3/ticker/24hr",
    "rolling_ticker": "/api/v3/ticker",
    "avg_price": "/api/v3/avgPrice",
    "recent_trades": "/api/v3/trades",
    "agg_trades": "/api/v3/aggTrades",
    "book_ticker": "/api/v3/ticker/bookTicker",
}
FORBIDDEN_ENDPOINTS = {
    "/api/v3/account",
    "/api/v3/order",
    "/api/v3/openOrders",
    "/api/v3/userDataStream",
}


@dataclass(frozen=True)
class IngestionRequest:
    symbols: list[str]
    intervals: list[str] = field(default_factory=lambda: ["1m", "5m", "15m", "1h"])
    candle_limit: int = 120
    include_exchange_info: bool = True
    include_order_book: bool = True
    include_24h_ticker: bool = True
    include_rolling_ticker: bool = True
    include_trades: bool = True
    use_cache: bool = True
    max_age_seconds: int = 300
    offline_ok: bool = True


@dataclass
class SymbolDataBundle:
    symbol: str
    filters: dict[str, Any] = field(default_factory=dict)
    candles: dict[str, list[Candle]] = field(default_factory=dict)
    order_book: dict[str, Any] = field(default_factory=dict)
    ticker_24h: dict[str, Any] = field(default_factory=dict)
    rolling_ticker: dict[str, Any] = field(default_factory=dict)
    recent_trades: list[dict[str, Any]] = field(default_factory=list)
    fetched_at_ms: int = 0
    source: str = "public-rest"
    warnings: list[dict[str, Any]] = field(default_factory=list)
    freshness_score: int = 100
    quality: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["candles"] = {
            interval: [asdict(candle) for candle in rows]
            for interval, rows in self.candles.items()
        }
        return redact_payload(payload)


@dataclass(frozen=True)
class IngestionResult:
    status: str
    bundles: list[SymbolDataBundle]
    manifests: list[str]
    warnings: list[dict[str, Any]] = field(default_factory=list)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(
            {
                "status": self.status,
                "bundles": [bundle.to_dict() for bundle in self.bundles],
                "manifests": self.manifests,
                "warnings": self.warnings,
                "live_trading_enabled": False,
                "public_endpoints": sorted(PUBLIC_ENDPOINTS.values()),
                "forbidden_endpoints": sorted(FORBIDDEN_ENDPOINTS),
            }
        )


class BinanceDataIngestionService:
    def __init__(self, settings: BotSettings, adapter: BinanceSpotAdapter | None = None, store: DataStore | None = None):
        self.settings = settings
        self.adapter = adapter or BinanceSpotAdapter(settings)
        self.store = store or DataStore(settings.data_dir)

    def ingest(self, request: IngestionRequest) -> IngestionResult:
        if self.settings.live_trading_enabled:
            return IngestionResult("blocked", [], [], [{"reason": "live trading enabled"}])
        bundles = []
        manifests = []
        warnings = []
        for symbol in _normalize_symbols(request.symbols):
            try:
                bundle = self._fetch_symbol(symbol, request)
            except Exception as exc:
                cached = self.load_cached_bundle(symbol, request.max_age_seconds)
                if cached and request.offline_ok:
                    cached.source = "cache-fallback"
                    cached.warnings.append({"reason": "public_rest_failed", "error": str(exc)})
                    bundle = cached
                else:
                    warnings.append({"symbol": symbol, "reason": "fetch_failed", "error": str(exc)})
                    continue
            path = self.save_public_data_bundle(bundle)
            manifests.append(str(path))
            bundles.append(bundle)
        return IngestionResult("ok" if bundles else "blocked", bundles, manifests, warnings)

    def load_cached_bundle(self, symbol: str, max_age_seconds: int = 300) -> SymbolDataBundle | None:
        manifest_dir = self.store.public_dir / "manifests"
        files = sorted(manifest_dir.glob(f"{symbol.upper()}-*.json"))
        if not files:
            return None
        payload = json.loads(files[-1].read_text(encoding="utf-8"))
        fetched_at = int(payload.get("fetched_at_ms", 0) or 0)
        if max_age_seconds >= 0 and int(time.time() * 1000) - fetched_at > max_age_seconds * 1000:
            return None
        bundle_path = Path(str((payload.get("files") or {}).get("bundle", "")))
        if not bundle_path.exists():
            return None
        raw = json.loads(bundle_path.read_text(encoding="utf-8"))
        candles = {
            interval: parse_binance_klines(rows)
            for interval, rows in (raw.get("raw_klines") or {}).items()
        }
        return SymbolDataBundle(
            symbol=raw["symbol"],
            filters=raw.get("filters", {}),
            candles=candles,
            order_book=raw.get("order_book", {}),
            ticker_24h=raw.get("ticker_24h", {}),
            rolling_ticker=raw.get("rolling_ticker", {}),
            recent_trades=raw.get("recent_trades", []),
            fetched_at_ms=fetched_at,
            source="cache",
            freshness_score=_freshness_score(fetched_at),
            quality=raw.get("quality", {}),
        )

    def save_public_data_bundle(self, bundle: SymbolDataBundle) -> Path:
        raw_klines = {
            interval: [
                [
                    candle.open_time_ms,
                    str(candle.open),
                    str(candle.high),
                    str(candle.low),
                    str(candle.close),
                    str(candle.volume),
                    candle.close_time_ms,
                    str(candle.quote_volume),
                    candle.trade_count,
                ]
                for candle in rows
            ]
            for interval, rows in bundle.candles.items()
        }
        stamp = str(bundle.fetched_at_ms)
        symbol = bundle.symbol.upper()
        bundle_payload = {
            "symbol": symbol,
            "filters": bundle.filters,
            "raw_klines": raw_klines,
            "order_book": bundle.order_book,
            "ticker_24h": bundle.ticker_24h,
            "rolling_ticker": bundle.rolling_ticker,
            "recent_trades": bundle.recent_trades,
            "quality": bundle.quality,
            "live_trading_enabled": False,
        }
        bundle_path = self.store.save_public_json("bundles", f"{symbol}-{stamp}", bundle_payload)
        files = {"bundle": str(bundle_path)}
        for interval, rows in bundle.candles.items():
            files[f"klines_{interval}"] = str(self.store.save_candles_csv(symbol, interval, rows))
        manifest = {
            "symbol": symbol,
            "intervals": sorted(bundle.candles.keys()),
            "files": files,
            "fetched_at_ms": bundle.fetched_at_ms,
            "source_endpoint": "public-rest/cache",
            "row_counts": {interval: len(rows) for interval, rows in bundle.candles.items()},
            "freshness_score": bundle.freshness_score,
            "warnings": bundle.warnings,
            "live_trading_enabled": False,
        }
        return self.store.save_data_manifest(f"{symbol}-{stamp}", manifest)

    def cache_status(self) -> dict[str, Any]:
        return self.store.cache_status()

    def clear_cache(self, confirm: str) -> dict[str, Any]:
        return self.store.clear_public_cache(confirm)

    def _fetch_symbol(self, symbol: str, request: IngestionRequest) -> SymbolDataBundle:
        fetched_at = int(time.time() * 1000)
        filters = self.adapter.get_exchange_info([symbol]) if request.include_exchange_info else {}
        candles = {
            interval: parse_binance_klines(self.adapter.get_klines(symbol, interval, limit=min(max(request.candle_limit, 1), 1000)))
            for interval in request.intervals
        }
        order_book = self.adapter.get_order_book(symbol, depth=20) if request.include_order_book else {}
        ticker_24h = self.adapter.get_24hr_ticker(symbol) if request.include_24h_ticker else {}
        rolling = self.adapter.get_rolling_ticker(symbol, "1h") if request.include_rolling_ticker else {}
        trades = self.adapter.get_recent_trades(symbol, limit=100) if request.include_trades else []
        bundle = SymbolDataBundle(
            symbol=symbol,
            filters=filters,
            candles=candles,
            order_book=order_book,
            ticker_24h=ticker_24h if isinstance(ticker_24h, dict) else {},
            rolling_ticker=rolling,
            recent_trades=trades,
            fetched_at_ms=fetched_at,
            freshness_score=100,
        )
        bundle.quality = bundle_quality(bundle.__dict__)
        return bundle


def export_public_data_evidence(settings: BotSettings, result: IngestionResult | None = None) -> Path:
    store = DataStore(settings.data_dir)
    payload = result.to_dict() if result else {"cache_status": store.cache_status(), "live_trading_enabled": False}
    path = store.public_dir / "public_data_manifest.json"
    path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return path


def _normalize_symbols(symbols: list[str]) -> list[str]:
    seen = set()
    rows = []
    for symbol in symbols:
        normalized = symbol.strip().upper()
        if normalized and normalized not in seen:
            rows.append(normalized)
            seen.add(normalized)
    return rows


def _freshness_score(fetched_at_ms: int) -> int:
    age_seconds = max(0, int(time.time() * 1000) - fetched_at_ms) / 1000
    return max(0, min(100, int(100 - age_seconds / 60)))

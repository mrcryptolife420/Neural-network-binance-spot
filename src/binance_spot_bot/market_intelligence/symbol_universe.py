from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from binance_spot_bot.redaction import redact_payload
from .public_endpoint_policy import NO_FINANCIAL_ADVICE_STATEMENT, NO_LIVE_STATEMENT, PUBLIC_DATA_ONLY_STATEMENT


@dataclass(frozen=True)
class SymbolUniverseEntry:
    symbol: str
    base_asset: str
    quote_asset: str
    status: str = "TRADING"
    is_spot_trading_allowed: bool = True
    order_types: tuple[str, ...] = ()
    tick_size: str = ""
    step_size: str = ""
    min_qty: str = ""
    max_qty: str = ""
    min_notional: str = ""
    updated_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))


@dataclass(frozen=True)
class SymbolUniverseFilter:
    quote_assets: tuple[str, ...] = ("USDT",)
    status: str = "TRADING"
    exclude_leveraged_tokens: bool = True
    include_symbols: tuple[str, ...] = ()
    exclude_symbols: tuple[str, ...] = ()
    max_symbols: int = 50


@dataclass(frozen=True)
class SymbolUniverseSnapshot:
    symbols: tuple[SymbolUniverseEntry, ...]
    source: str = "fixture"
    updated_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    no_live_statement: str = NO_LIVE_STATEMENT
    public_data_only_statement: str = PUBLIC_DATA_ONLY_STATEMENT
    no_financial_advice_statement: str = NO_FINANCIAL_ADVICE_STATEMENT
    live_trading_enabled: bool = False


def demo_exchange_info() -> dict[str, Any]:
    symbols = []
    for symbol, base, quote in [("BTCUSDT", "BTC", "USDT"), ("ETHUSDT", "ETH", "USDT"), ("BNBUSDT", "BNB", "USDT"), ("SOLUSDT", "SOL", "USDT"), ("XRPUSDT", "XRP", "USDT")]:
        symbols.append(
            {
                "symbol": symbol,
                "baseAsset": base,
                "quoteAsset": quote,
                "status": "TRADING",
                "isSpotTradingAllowed": True,
                "orderTypes": ["LIMIT", "MARKET"],
                "filters": [
                    {"filterType": "PRICE_FILTER", "tickSize": "0.01"},
                    {"filterType": "LOT_SIZE", "stepSize": "0.0001", "minQty": "0.0001", "maxQty": "1000"},
                    {"filterType": "MIN_NOTIONAL", "minNotional": "5"},
                ],
            }
        )
    return {"symbols": symbols}


def _filter_value(filters: list[dict[str, Any]], filter_type: str, key: str) -> str:
    for item in filters:
        if item.get("filterType") == filter_type:
            return str(item.get(key, ""))
    return ""


def build_symbol_universe(exchange_info: dict[str, Any] | None = None, filter_config: SymbolUniverseFilter | None = None) -> SymbolUniverseSnapshot:
    exchange_info = exchange_info or demo_exchange_info()
    filter_config = filter_config or SymbolUniverseFilter()
    rows: list[SymbolUniverseEntry] = []
    for raw in exchange_info.get("symbols", []):
        symbol = str(raw.get("symbol", "")).upper()
        base = str(raw.get("baseAsset", "")).upper()
        quote = str(raw.get("quoteAsset", "")).upper()
        if quote not in filter_config.quote_assets or raw.get("status") != filter_config.status:
            continue
        if symbol in filter_config.exclude_symbols:
            continue
        if filter_config.include_symbols and symbol not in filter_config.include_symbols:
            continue
        if filter_config.exclude_leveraged_tokens and any(tag in base for tag in ("UP", "DOWN", "BULL", "BEAR")):
            continue
        filters = raw.get("filters", [])
        rows.append(
            SymbolUniverseEntry(
                symbol=symbol,
                base_asset=base,
                quote_asset=quote,
                status=str(raw.get("status", "")),
                is_spot_trading_allowed=bool(raw.get("isSpotTradingAllowed", True)),
                order_types=tuple(str(item) for item in raw.get("orderTypes", [])),
                tick_size=_filter_value(filters, "PRICE_FILTER", "tickSize"),
                step_size=_filter_value(filters, "LOT_SIZE", "stepSize"),
                min_qty=_filter_value(filters, "LOT_SIZE", "minQty"),
                max_qty=_filter_value(filters, "LOT_SIZE", "maxQty"),
                min_notional=_filter_value(filters, "MIN_NOTIONAL", "minNotional"),
            )
        )
    return SymbolUniverseSnapshot(symbols=tuple(rows[: max(1, filter_config.max_symbols)]))


def symbol_universe_to_dict(snapshot: SymbolUniverseSnapshot) -> dict[str, Any]:
    return redact_payload(asdict(snapshot) | {"status": "ok", "count": len(snapshot.symbols)})


def write_symbol_universe_report(root: Path | str = ".") -> dict[str, Any]:
    out = Path(root) / "data" / "market-intelligence" / "symbol-universe"
    out.mkdir(parents=True, exist_ok=True)
    snapshot = build_symbol_universe()
    payload = symbol_universe_to_dict(snapshot)
    json_path = out / "symbol_universe_latest.json"
    md_path = out / "symbol_universe_report.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(f"# Symbol Universe\n\nSymbols: {payload['count']}\n\n{NO_FINANCIAL_ADVICE_STATEMENT}\n", encoding="utf-8")
    return {"status": "ok", "json": str(json_path), "markdown": str(md_path), "report": payload, "live_trading_enabled": False}

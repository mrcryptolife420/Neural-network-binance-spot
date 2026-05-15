from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from binance_spot_bot.redaction import redact_payload
from .market_metrics import compute_market_metrics, market_metrics_to_dict
from .market_snapshot_cache import default_market_snapshot_cache, demo_market_snapshot
from .public_endpoint_policy import NO_FINANCIAL_ADVICE_STATEMENT, NO_LIVE_STATEMENT, PUBLIC_DATA_ONLY_STATEMENT
from .rate_limit_budget import scanner_rate_limit_plan


@dataclass(frozen=True)
class WatchlistSymbolSnapshot:
    symbol: str
    status: str
    last_price: str
    bid: str
    ask: str
    spread_bps: str
    quote_volume_24h: str
    price_change_percent_24h: str
    data_quality_status: str
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class WatchlistScanRun:
    run_id: str
    symbols: tuple[WatchlistSymbolSnapshot, ...]
    metrics: tuple[dict[str, Any], ...]
    source: str = "fixture"
    no_live_statement: str = NO_LIVE_STATEMENT
    public_data_only_statement: str = PUBLIC_DATA_ONLY_STATEMENT
    no_financial_advice_statement: str = NO_FINANCIAL_ADVICE_STATEMENT
    live_trading_enabled: bool = False


def run_watchlist_scan(symbols: list[str] | tuple[str, ...], *, root: Path | str = ".", preset: str = "majors_overview") -> dict[str, Any]:
    plan = scanner_rate_limit_plan(symbols)
    if plan["status"] == "blocked":
        return plan
    cache = default_market_snapshot_cache(root)
    rows: list[WatchlistSymbolSnapshot] = []
    metrics_rows: list[dict[str, Any]] = []
    for symbol in symbols:
        symbol = symbol.upper()
        snapshot = cache.load("ticker", symbol)
        payload = snapshot.get("payload") if snapshot.get("status") in {"fresh", "stale"} else demo_market_snapshot(symbol)
        metrics = compute_market_metrics(payload)
        metrics_rows.append(market_metrics_to_dict(metrics))
        rows.append(
            WatchlistSymbolSnapshot(
                symbol=symbol,
                status="ok",
                last_price=str(payload.get("lastPrice", "")),
                bid=str(payload.get("bidPrice", "")),
                ask=str(payload.get("askPrice", "")),
                spread_bps=metrics.spread_bps,
                quote_volume_24h=metrics.quote_volume_24h,
                price_change_percent_24h=metrics.price_change_24h,
                data_quality_status="ok" if metrics.data_quality_score >= 75 else "warn",
                warnings=metrics.warnings,
            )
        )
    run = WatchlistScanRun(str(int(time.time() * 1000)), tuple(rows), tuple(metrics_rows))
    out = Path(root) / "data" / "market-intelligence" / "scan-runs"
    out.mkdir(parents=True, exist_ok=True)
    payload = redact_payload(asdict(run) | {"status": "ok", "preset": preset})
    (out / f"{run.run_id}.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return payload

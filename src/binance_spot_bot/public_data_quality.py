from __future__ import annotations

import time
from decimal import Decimal
from typing import Any

from .types import Candle


def candle_quality(candles: list[Candle], *, min_candles: int = 30, now_ms: int | None = None) -> dict[str, Any]:
    now = now_ms or int(time.time() * 1000)
    warnings: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []
    if len(candles) < min_candles:
        blockers.append({"check": "candle_count", "reason": f"{len(candles)} < {min_candles}"})
    timestamps = [candle.open_time_ms for candle in candles]
    if len(set(timestamps)) != len(timestamps):
        blockers.append({"check": "duplicate_candles", "reason": "duplicate open_time_ms"})
    if any(left >= right for left, right in zip(timestamps, timestamps[1:])):
        blockers.append({"check": "chronology", "reason": "candles not strictly chronological"})
    invalid = [candle for candle in candles if candle.low > candle.high or not (candle.low <= candle.open <= candle.high and candle.low <= candle.close <= candle.high)]
    if invalid:
        blockers.append({"check": "ohlc", "reason": f"{len(invalid)} invalid OHLC rows"})
    zero_volume = sum(1 for candle in candles if candle.volume <= 0)
    if zero_volume:
        warnings.append({"check": "zero_volume", "reason": f"{zero_volume} zero volume candles"})
    age_ms = now - candles[-1].close_time_ms if candles else None
    if age_ms is not None and age_ms > 15 * 60 * 1000:
        warnings.append({"check": "stale_latest_candle", "reason": f"{age_ms}ms old"})
    status = "blocked" if blockers else "warning" if warnings else "healthy"
    score = max(0, 100 - len(blockers) * 40 - len(warnings) * 10)
    return {"status": status, "score": score, "blockers": blockers, "warnings": warnings, "latest_age_ms": age_ms}


def order_book_liquidity(order_book: dict[str, Any], quote_sizes: tuple[Decimal, ...] = (Decimal("10"), Decimal("25"), Decimal("50"), Decimal("100"))) -> dict[str, Any]:
    bids = _levels(order_book.get("bids", []))
    asks = _levels(order_book.get("asks", []))
    if not bids or not asks:
        return {"status": "blocked", "reason": "empty_order_book", "score": 0}
    best_bid = bids[0][0]
    best_ask = asks[0][0]
    mid = (best_bid + best_ask) / Decimal("2")
    spread_bps = ((best_ask - best_bid) / mid * Decimal("10000")) if mid else Decimal("0")
    bid_liquidity_5 = sum(price * qty for price, qty in bids[:5])
    ask_liquidity_5 = sum(price * qty for price, qty in asks[:5])
    bid_liquidity_20 = sum(price * qty for price, qty in bids[:20])
    ask_liquidity_20 = sum(price * qty for price, qty in asks[:20])
    total_20 = bid_liquidity_20 + ask_liquidity_20
    imbalance = ((bid_liquidity_20 - ask_liquidity_20) / total_20) if total_20 else Decimal("0")
    slippage = {str(size): str(_estimate_slippage(asks, size, best_ask)) for size in quote_sizes}
    thin = bid_liquidity_5 < Decimal("100") or ask_liquidity_5 < Decimal("100")
    score = max(0, min(100, 100 - float(spread_bps) * 2 - (25 if thin else 0)))
    return {
        "status": "warning" if thin or spread_bps > Decimal("20") else "healthy",
        "best_bid": str(best_bid),
        "best_ask": str(best_ask),
        "spread_bps": float(round(spread_bps, 6)),
        "bid_liquidity_top_5": str(bid_liquidity_5),
        "ask_liquidity_top_5": str(ask_liquidity_5),
        "bid_liquidity_top_20": str(bid_liquidity_20),
        "ask_liquidity_top_20": str(ask_liquidity_20),
        "order_book_imbalance": float(round(imbalance, 6)),
        "estimated_slippage_bps": slippage,
        "thin_book_warning": thin,
        "score": round(score, 2),
    }


def ticker_context(ticker_24h: dict[str, Any] | None, rolling: dict[str, Any] | None = None) -> dict[str, Any]:
    ticker = ticker_24h or {}
    rolling = rolling or {}
    quote_volume = _decimal(ticker.get("quoteVolume"))
    trade_count = int(ticker.get("count") or ticker.get("tradeCount") or 0)
    change = float(ticker.get("priceChangePercent") or 0)
    rolling_change = float(rolling.get("priceChangePercent") or rolling.get("priceChange") or 0)
    volume_score = min(100.0, float(quote_volume / Decimal("100000")) if quote_volume else 0.0)
    return {
        "status": "healthy" if quote_volume > Decimal("10000") else "warning",
        "price_change_percent_24h": change,
        "quote_volume_24h": str(quote_volume),
        "trade_count_24h": trade_count,
        "weighted_avg_price": str(ticker.get("weightedAvgPrice", "")),
        "rolling_change": rolling_change,
        "volume_score": round(volume_score, 2),
    }


def trade_flow_features(trades: list[dict[str, Any]]) -> dict[str, Any]:
    qtys = [_decimal(item.get("qty") or item.get("q")) for item in trades]
    notionals = [_decimal(item.get("price") or item.get("p")) * qty for item, qty in zip(trades, qtys)]
    avg_size = sum(notionals) / Decimal(len(notionals)) if notionals else Decimal("0")
    large = sum(1 for value in notionals if value >= avg_size * Decimal("3") and value > 0)
    burst = min(100, len(trades))
    return {
        "status": "healthy" if trades else "missing",
        "recent_trade_count": len(trades),
        "average_trade_size_quote": str(avg_size),
        "large_trade_count": large,
        "trade_burst_score": burst,
        "confidence_adjustment": min(0.05, burst / 2000),
    }


def bundle_quality(bundle: dict[str, Any], *, min_candles: int = 30, now_ms: int | None = None) -> dict[str, Any]:
    candle_reports = {
        interval: candle_quality(candles, min_candles=min_candles, now_ms=now_ms)
        for interval, candles in (bundle.get("candles") or {}).items()
    }
    liquidity = order_book_liquidity(bundle.get("order_book") or {}) if bundle.get("order_book") else {"status": "missing", "score": 0}
    ticker = ticker_context(bundle.get("ticker_24h") or {}, bundle.get("rolling_ticker") or {})
    flow = trade_flow_features(bundle.get("recent_trades") or [])
    statuses = [item["status"] for item in candle_reports.values()] + [liquidity["status"], ticker["status"], flow["status"]]
    status = "blocked" if "blocked" in statuses else "degraded" if "missing" in statuses else "warning" if "warning" in statuses else "healthy"
    return {"status": status, "candles": candle_reports, "liquidity": liquidity, "market_context": ticker, "flow": flow}


def _levels(rows: list[Any]) -> list[tuple[Decimal, Decimal]]:
    return [(Decimal(str(row[0])), Decimal(str(row[1]))) for row in rows]


def _estimate_slippage(asks: list[tuple[Decimal, Decimal]], quote_size: Decimal, best_ask: Decimal) -> Decimal:
    remaining = quote_size
    qty = Decimal("0")
    spent = Decimal("0")
    for price, level_qty in asks:
        level_quote = price * level_qty
        take_quote = min(remaining, level_quote)
        qty += take_quote / price
        spent += take_quote
        remaining -= take_quote
        if remaining <= 0:
            break
    if qty <= 0 or spent <= 0:
        return Decimal("9999")
    avg = spent / qty
    return ((avg - best_ask) / best_ask * Decimal("10000")).quantize(Decimal("0.0001"))


def _decimal(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")

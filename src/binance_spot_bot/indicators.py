from __future__ import annotations

import json
import time
from decimal import Decimal
from pathlib import Path
from statistics import mean
from typing import Any

from .redaction import redact_payload
from .types import Candle

INDICATOR_PROFILES = ("auto", "trend", "momentum", "volatility", "range")


def ema(values: list[float], period: int) -> float:
    if not values:
        return 0.0
    alpha = 2 / (period + 1)
    current = values[0]
    for value in values[1:]:
        current = value * alpha + current * (1 - alpha)
    return current


def rsi(values: list[float], period: int = 14) -> float:
    if len(values) <= period:
        return 50.0
    gains: list[float] = []
    losses: list[float] = []
    for prev, current in zip(values[-period - 1 : -1], values[-period:]):
        delta = current - prev
        gains.append(max(delta, 0.0))
        losses.append(abs(min(delta, 0.0)))
    avg_gain = mean(gains) if gains else 0.0
    avg_loss = mean(losses) if losses else 0.0
    if avg_loss == 0:
        return 100.0 if avg_gain else 50.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def atr(candles: list[Candle], period: int = 14) -> float:
    if len(candles) < 2:
        return 0.0
    ranges: list[float] = []
    recent = candles[-period:]
    previous_close = float(candles[-len(recent) - 1].close) if len(candles) > len(recent) else float(recent[0].close)
    for candle in recent:
        high = float(candle.high)
        low = float(candle.low)
        ranges.append(max(high - low, abs(high - previous_close), abs(low - previous_close)))
        previous_close = float(candle.close)
    return mean(ranges) if ranges else 0.0


def macd(values: list[float]) -> dict[str, float]:
    if not values:
        return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}
    line = ema(values, 12) - ema(values, 26)
    signal = ema([ema(values[: index + 1], 12) - ema(values[: index + 1], 26) for index in range(len(values))], 9)
    return {"macd": line, "signal": signal, "histogram": line - signal}


def bollinger_position(values: list[float], period: int = 20) -> float:
    if len(values) < period:
        return 0.5
    recent = values[-period:]
    avg = mean(recent)
    variance = mean([(value - avg) ** 2 for value in recent])
    std = variance**0.5
    if std == 0:
        return 0.5
    lower = avg - 2 * std
    upper = avg + 2 * std
    return max(0.0, min(1.0, (values[-1] - lower) / (upper - lower)))


def detect_regime(candles: list[Candle]) -> dict[str, str]:
    if len(candles) < 30:
        return {"regime": "insufficient_data", "reason": "Need at least 30 candles"}
    closes = [float(c.close) for c in candles]
    fast = ema(closes, 12)
    slow = ema(closes, 26)
    current_atr = atr(candles)
    price = closes[-1] or 1.0
    atr_pct = current_atr / price
    trend_pct = (fast - slow) / price
    if atr_pct > 0.012:
        return {"regime": "high_volatility", "reason": "ATR is elevated"}
    if trend_pct > 0.002:
        return {"regime": "uptrend", "reason": "EMA fast is above EMA slow"}
    if trend_pct < -0.002:
        return {"regime": "downtrend", "reason": "EMA fast is below EMA slow"}
    return {"regime": "range", "reason": "EMA spread is small"}


def choose_indicator_profile(candles: list[Candle], requested: str = "auto") -> str:
    if requested != "auto":
        return requested if requested in INDICATOR_PROFILES else "trend"
    regime = detect_regime(candles)["regime"]
    if regime in {"uptrend", "downtrend"}:
        return "trend"
    if regime == "high_volatility":
        return "volatility"
    if regime == "range":
        return "range"
    return "momentum"


def indicator_snapshot(symbol: str, candles: list[Candle], requested_profile: str = "auto") -> dict[str, Any]:
    closes = [float(candle.close) for candle in candles]
    regime = detect_regime(candles)
    profile = choose_indicator_profile(candles, requested_profile)
    macd_payload = macd(closes)
    row = {
        "symbol": symbol,
        "profile": profile,
        "requested_profile": requested_profile,
        "regime": regime["regime"],
        "regime_reason": regime["reason"],
        "ema_fast": round(ema(closes, 12), 6),
        "ema_slow": round(ema(closes, 26), 6),
        "rsi": round(rsi(closes), 2),
        "atr": round(atr(candles), 6),
        "macd_histogram": round(macd_payload["histogram"], 6),
        "bollinger_position": round(bollinger_position(closes), 4),
    }
    row.update(indicator_advice(row))
    row["live_trading_enabled"] = False
    return row


def indicator_advice(row: dict[str, Any]) -> dict[str, Any]:
    score = 0.0
    reasons: list[str] = []
    if float(row.get("ema_fast", 0)) > float(row.get("ema_slow", 0)):
        score += 0.3
        reasons.append("EMA trend up")
    else:
        score -= 0.3
        reasons.append("EMA trend down")
    if float(row.get("macd_histogram", 0)) > 0:
        score += 0.25
        reasons.append("MACD positive")
    elif float(row.get("macd_histogram", 0)) < 0:
        score -= 0.25
        reasons.append("MACD negative")
    current_rsi = float(row.get("rsi", 50))
    if current_rsi < 35:
        score += 0.2
        reasons.append("RSI oversold")
    elif current_rsi > 70:
        score -= 0.2
        reasons.append("RSI overbought")
    side = "BUY" if score > 0.25 else "SELL" if score < -0.25 else "HOLD"
    return {"bias": side, "confidence": round(min(1.0, abs(score)), 3), "reason": "; ".join(reasons) or "Neutral indicators"}


def indicator_rows_from_runtimes(runtimes: dict[str, Any], requested_profile: str = "auto") -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for symbol, runtime in runtimes.items():
        snapshot = runtime.snapshot()
        rows.append(indicator_snapshot(symbol, snapshot.candles, requested_profile))
    return rows


def indicator_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    bias_counts: dict[str, int] = {}
    regime_counts: dict[str, int] = {}
    confidence_values: list[float] = []
    for row in rows:
        bias_counts[str(row.get("bias", "HOLD"))] = bias_counts.get(str(row.get("bias", "HOLD")), 0) + 1
        regime_counts[str(row.get("regime", "unknown"))] = regime_counts.get(str(row.get("regime", "unknown")), 0) + 1
        confidence_values.append(float(row.get("confidence", 0)))
    return {
        "symbols": len(rows),
        "bias_counts": bias_counts,
        "regime_counts": regime_counts,
        "avg_confidence": round(mean(confidence_values), 4) if confidence_values else 0.0,
        "live_trading_enabled": False,
    }


def allocation_hints(rows: list[dict[str, Any]], total_quote_budget: Decimal) -> list[dict[str, str]]:
    if not rows:
        return []
    weights: list[Decimal] = []
    for row in rows:
        confidence = Decimal(str(row.get("confidence", 0)))
        weight = Decimal("0.2") if row.get("bias") == "HOLD" else Decimal("0.5") + confidence
        if row.get("regime") == "high_volatility":
            weight *= Decimal("0.5")
        weights.append(weight)
    total_weight = sum(weights) or Decimal("1")
    return [
        {
            "symbol": str(row.get("symbol")),
            "bias": str(row.get("bias")),
            "suggested_quote": str(((weight / total_weight) * total_quote_budget).quantize(Decimal("0.01"))),
            "note": "informational only",
        }
        for row, weight in zip(rows, weights)
    ]


def write_indicator_evidence(data_dir: Path, rows: list[dict[str, Any]], profile: str, auto_profile: bool) -> dict[str, Any]:
    path = data_dir / "evidence" / "indicators" / "indicator-advisor.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = redact_payload(
        {
            "created_at_ms": int(time.time() * 1000),
            "profile": profile,
            "auto_profile": auto_profile,
            "rows": rows,
            "summary": indicator_summary(rows),
            "live_trading_enabled": False,
        }
    )
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return {"status": "ok", "path": str(path), "live_trading_enabled": False}

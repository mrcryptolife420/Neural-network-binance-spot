from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

from binance_spot_bot.redaction import redact_payload


def _dec(value: Any, default: str = "0") -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return Decimal(default)


@dataclass(frozen=True)
class MarketMetricSet:
    symbol: str
    spread_bps: str
    quote_volume_24h: str
    base_volume_24h: str
    price_change_24h: str
    high_low_range_24h: str
    intraday_volatility: str
    candle_momentum: str
    liquidity_proxy: str
    data_quality_score: int
    warnings: tuple[str, ...] = ()


def compute_market_metrics(snapshot: dict[str, Any]) -> MarketMetricSet:
    symbol = str(snapshot.get("symbol", "UNKNOWN"))
    bid = _dec(snapshot.get("bidPrice"))
    ask = _dec(snapshot.get("askPrice"))
    last = _dec(snapshot.get("lastPrice"), "1") or Decimal("1")
    spread_bps = ((ask - bid) / last * Decimal("10000")) if ask and bid else Decimal("0")
    high = _dec(snapshot.get("highPrice"))
    low = _dec(snapshot.get("lowPrice"))
    range_pct = ((high - low) / last * Decimal("100")) if high and low else Decimal("0")
    klines = snapshot.get("klines", [])
    closes = [_dec(row[4]) for row in klines if isinstance(row, list) and len(row) > 4]
    momentum = closes[-1] - closes[0] if len(closes) >= 2 else Decimal("0")
    volatility = max(closes) - min(closes) if closes else Decimal("0")
    warnings = []
    if not klines:
        warnings.append("missing klines")
    score = 100 - min(50, len(warnings) * 25)
    return MarketMetricSet(
        symbol=symbol,
        spread_bps=str(spread_bps.quantize(Decimal("0.01"))),
        quote_volume_24h=str(_dec(snapshot.get("quoteVolume"))),
        base_volume_24h=str(_dec(snapshot.get("volume"))),
        price_change_24h=str(_dec(snapshot.get("priceChangePercent"))),
        high_low_range_24h=str(range_pct.quantize(Decimal("0.01"))),
        intraday_volatility=str(volatility),
        candle_momentum=str(momentum),
        liquidity_proxy=str((_dec(snapshot.get("quoteVolume")) / max(Decimal("1"), spread_bps + Decimal("1"))).quantize(Decimal("0.01"))),
        data_quality_score=score,
        warnings=tuple(warnings),
    )


def market_metrics_to_dict(metrics: MarketMetricSet) -> dict[str, Any]:
    return redact_payload(asdict(metrics))

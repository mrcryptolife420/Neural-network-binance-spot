from __future__ import annotations

from decimal import Decimal
from typing import Any

from binance_spot_bot.redaction import redact_payload
from .public_endpoint_policy import NO_FINANCIAL_ADVICE_STATEMENT, NO_LIVE_STATEMENT

FORBIDDEN_ADVICE_WORDS = ("buy now", "sell now", "best coin to trade", "guaranteed")


def _dec(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def rank_symbols(metrics: list[dict[str, Any]], dimension: str = "quote_volume_24h", limit: int = 10) -> dict[str, Any]:
    key = {
        "highest_quote_volume": "quote_volume_24h",
        "lowest_spread": "spread_bps",
        "highest_volatility": "intraday_volatility",
        "freshest_data": "data_quality_score",
        "liquidity_proxy": "liquidity_proxy",
    }.get(dimension, dimension)
    reverse = dimension != "lowest_spread"
    ranked = sorted(metrics, key=lambda item: _dec(item.get(key, 0)), reverse=reverse)[:limit]
    payload = {
        "status": "ok",
        "dimension": dimension,
        "wording": "ranked by metric for research only",
        "ranks": [{"rank": idx + 1, "symbol": item.get("symbol"), "value": item.get(key)} for idx, item in enumerate(ranked)],
        "no_financial_advice_statement": NO_FINANCIAL_ADVICE_STATEMENT,
        "no_live_statement": NO_LIVE_STATEMENT,
        "live_trading_enabled": False,
    }
    text = str(payload).lower()
    if any(word in text for word in FORBIDDEN_ADVICE_WORDS):
        return {"status": "blocked", "blockers": ["financial advice wording detected"], "live_trading_enabled": False}
    return redact_payload(payload)

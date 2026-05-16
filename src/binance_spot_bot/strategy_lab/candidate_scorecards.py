from __future__ import annotations

from decimal import Decimal
from typing import Any

from binance_spot_bot.redaction import redact_payload
from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT

FORBIDDEN_WORDS = ("buy", "sell", "sure win", "best trade")


def _dec(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def build_candidate_scorecards(results: list[dict[str, Any]], candidates: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    by_symbol = {str(item.get("symbol")): item for item in candidates or []}
    cards = []
    for row in results:
        metric = by_symbol.get(str(row.get("symbol")), {}).get("metrics_snapshot", {})
        quality = int(metric.get("data_quality_score", 75) or 75)
        spread_penalty = min(30, int(_dec(metric.get("spread_bps", 0))))
        pnl_score = max(0, min(40, int((_dec(row.get("paper_pnl")) + Decimal("1")) * 20)))
        drawdown_penalty = min(30, abs(int(_dec(row.get("max_drawdown")) * 10)))
        score = max(0, min(100, quality // 2 + pnl_score - spread_penalty - drawdown_penalty))
        cards.append(
            {
                "candidate_id": row.get("candidate_id", row.get("job_id")),
                "symbol": row.get("symbol"),
                "paper_only_score": score,
                "market_quality_score": quality,
                "paper_performance_score": pnl_score,
                "drawdown_penalty": drawdown_penalty,
                "warnings": row.get("data_quality_warnings", []),
                "wording": "research candidate",
            }
        )
    payload = {"status": "ok", "scorecards": sorted(cards, key=lambda item: item["paper_only_score"], reverse=True), "no_live_statement": NO_LIVE_STATEMENT, "no_advice_statement": NO_ADVICE_STATEMENT, "live_trading_enabled": False}
    if any(word in str(payload).lower() for word in FORBIDDEN_WORDS):
        return {"status": "blocked", "blockers": ["advice wording detected"], "live_trading_enabled": False}
    return redact_payload(payload)

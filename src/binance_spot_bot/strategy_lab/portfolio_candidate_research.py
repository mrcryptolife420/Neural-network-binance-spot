from __future__ import annotations

from collections import Counter
from typing import Any

from binance_spot_bot.redaction import redact_payload
from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT


def build_portfolio_candidate_research(scorecards: list[dict[str, Any]], *, max_candidates: int = 5) -> dict[str, Any]:
    selected = [row for row in scorecards if int(row.get("paper_only_score", 0)) >= 40][:max_candidates]
    quotes = Counter(str(row.get("symbol", ""))[-4:] for row in selected)
    warnings = []
    if len({str(row.get("symbol", ""))[:3] for row in selected}) < min(2, len(selected)):
        warnings.append("basket concentration warning")
    return redact_payload(
        {
            "status": "ok",
            "basket": selected,
            "quote_distribution": dict(quotes),
            "paper_only_allocation_note": "equal-weight research basket for later paper experiments",
            "risk_warnings": warnings,
            "no_live_statement": NO_LIVE_STATEMENT,
            "no_advice_statement": NO_ADVICE_STATEMENT,
            "live_trading_enabled": False,
        }
    )

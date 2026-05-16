from __future__ import annotations

from typing import Any

from .candidate_basket import PortfolioCandidateBasket


def analyze_allocation_decay(basket: PortfolioCandidateBasket) -> dict[str, Any]:
    rows = []
    for item in basket.items:
        deterioration = max(0.0, (100.0 - item.paper_score) / 100.0 + abs(item.max_drawdown))
        if deterioration > 0.45:
            status = "degraded"
        elif deterioration > 0.30:
            status = "watch"
        else:
            status = "stable"
        rows.append(
            {
                "item_id": item.item_id,
                "symbol": item.symbol,
                "decay_score": round(deterioration, 6),
                "status": status,
                "signals": ["paper_score_deterioration"] if status != "stable" else [],
                "live_trading_enabled": False,
            }
        )
    return {"status": "ok", "decay": rows, "live_trading_enabled": False}


from __future__ import annotations

from typing import Any

from .candidate_basket import PortfolioCandidateBasket


def portfolio_correlation_proxy(basket: PortfolioCandidateBasket) -> dict[str, Any]:
    matrix: list[dict[str, Any]] = []
    warnings: list[str] = []
    active = [item for item in basket.items if not item.disabled and not item.blocked_reason]
    for left in active:
        for right in active:
            if left.item_id >= right.item_id:
                continue
            same_strategy = left.strategy_id == right.strategy_id
            same_model = left.model_alias == right.model_alias
            score_gap = abs(left.paper_score - right.paper_score) / 100.0
            proxy = min(1.0, 0.25 + (0.25 if same_strategy else 0.0) + (0.25 if same_model else 0.0) + max(0.0, 0.25 - score_gap))
            if proxy > 0.70:
                warnings.append(f"high overlap proxy: {left.symbol}/{right.symbol}")
            matrix.append(
                {
                    "left": left.symbol,
                    "right": right.symbol,
                    "co_movement_proxy": round(proxy, 6),
                    "shared_strategy": same_strategy,
                    "shared_model": same_model,
                    "same_quote_asset_overlap": True,
                }
            )
    return {"status": "warn" if warnings else "ok", "basket_id": basket.basket_id, "matrix": matrix, "warnings": warnings, "live_trading_enabled": False}


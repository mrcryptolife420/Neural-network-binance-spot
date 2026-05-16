from __future__ import annotations

from typing import Any

from .candidate_basket import PortfolioCandidateBasket
from .common import stable_hash


def simulate_basket(
    basket: PortfolioCandidateBasket,
    allocation: dict[str, Any],
    *,
    starting_quote: float = 1000.0,
    periods: int = 48,
    mode: str = "static_allocation",
) -> dict[str, Any]:
    weights = {str(item["item_id"]): float(item["weight"]) for item in allocation.get("items", [])}
    item_by_id = {item.item_id: item for item in basket.items}
    equity = starting_quote
    curve: list[dict[str, Any]] = []
    contributions: dict[str, float] = {}
    peak = starting_quote
    max_drawdown = 0.0
    for step in range(periods + 1):
        if step > 0:
            weighted_return = 0.0
            for item_id, weight in weights.items():
                item = item_by_id[item_id]
                signal = ((item.paper_score / 1000.0) - abs(item.max_drawdown) / 8.0) + ((step % 7) - 3) * 0.00015
                contribution = equity * weight * signal
                contributions[item.symbol] = contributions.get(item.symbol, 0.0) + contribution
                weighted_return += weight * signal
            equity *= 1.0 + weighted_return
        peak = max(peak, equity)
        drawdown = 0.0 if peak <= 0 else (peak - equity) / peak
        max_drawdown = max(max_drawdown, drawdown)
        curve.append({"step": step, "equity": round(equity, 6), "drawdown": round(drawdown, 8)})
    returns = [(curve[idx]["equity"] / curve[idx - 1]["equity"] - 1.0) for idx in range(1, len(curve)) if curve[idx - 1]["equity"]]
    avg = sum(returns) / len(returns) if returns else 0.0
    variance = sum((item - avg) ** 2 for item in returns) / len(returns) if returns else 0.0
    return {
        "status": "ok",
        "simulation_id": f"simulation-{stable_hash({'basket': basket.basket_id, 'allocation': allocation.get('allocation_id'), 'mode': mode})[:12]}",
        "basket_id": basket.basket_id,
        "allocation_id": allocation.get("allocation_id"),
        "mode": mode,
        "starting_quote": starting_quote,
        "ending_quote": round(equity, 6),
        "paper_pnl": round(equity - starting_quote, 6),
        "max_drawdown": round(max_drawdown, 8),
        "volatility_proxy": round(variance ** 0.5, 8),
        "fees_estimate": round(starting_quote * 0.001 * max(1, len(weights)), 6),
        "turnover_estimate": round(sum(weights.values()) * 0.2, 6),
        "risk_budget_usage": round(max(weights.values()) if weights else 0.0, 8),
        "blocked_action_count": 0,
        "equity_curve": curve,
        "symbol_contributions": {symbol: round(value, 6) for symbol, value in contributions.items()},
        "live_trading_enabled": False,
    }


from __future__ import annotations

from typing import Any

from .candidate_basket import PortfolioCandidateBasket


def analyze_portfolio_risk(basket: PortfolioCandidateBasket, allocation: dict[str, Any], simulation: dict[str, Any]) -> dict[str, Any]:
    weights = {str(item["item_id"]): float(item["weight"]) for item in allocation.get("items", [])}
    items = {item.item_id: item for item in basket.items}
    exposure_by_symbol: dict[str, float] = {}
    exposure_by_strategy: dict[str, float] = {}
    exposure_by_model: dict[str, float] = {}
    exposure_by_volatility_bucket: dict[str, float] = {}
    data_quality_weighted = 0.0
    for item_id, weight in weights.items():
        item = items[item_id]
        exposure_by_symbol[item.symbol] = exposure_by_symbol.get(item.symbol, 0.0) + weight
        exposure_by_strategy[item.strategy_id] = exposure_by_strategy.get(item.strategy_id, 0.0) + weight
        exposure_by_model[item.model_alias] = exposure_by_model.get(item.model_alias, 0.0) + weight
        exposure_by_volatility_bucket[item.volatility_bucket] = exposure_by_volatility_bucket.get(item.volatility_bucket, 0.0) + weight
        data_quality_weighted += weight * item.data_quality_score
    max_weight = max(weights.values()) if weights else 0.0
    warnings = []
    if max_weight > 0.45:
        warnings.append("concentration warning")
    return {
        "status": "warn" if warnings else "ok",
        "portfolio_max_drawdown": simulation.get("max_drawdown", 0.0),
        "drawdown_duration": len([row for row in simulation.get("equity_curve", []) if row.get("drawdown", 0) > 0]),
        "volatility_proxy": simulation.get("volatility_proxy", 0.0),
        "return_drawdown_ratio": round(float(simulation.get("paper_pnl", 0.0)) / max(0.0001, float(simulation.get("max_drawdown", 0.0))), 6),
        "downside_deviation": simulation.get("volatility_proxy", 0.0),
        "concentration_score": round(max_weight, 8),
        "exposure_by_symbol": {key: round(value, 8) for key, value in exposure_by_symbol.items()},
        "exposure_by_strategy": {key: round(value, 8) for key, value in exposure_by_strategy.items()},
        "exposure_by_model_alias": {key: round(value, 8) for key, value in exposure_by_model.items()},
        "exposure_by_volatility_bucket": {key: round(value, 8) for key, value in exposure_by_volatility_bucket.items()},
        "data_quality_weighted_exposure": round(data_quality_weighted, 6),
        "risk_block_contribution": 0,
        "fee_drag": simulation.get("fees_estimate", 0.0),
        "turnover_proxy": simulation.get("turnover_estimate", 0.0),
        "warnings": warnings,
        "live_trading_enabled": False,
    }


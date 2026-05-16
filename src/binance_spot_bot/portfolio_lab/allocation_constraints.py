from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .candidate_basket import PortfolioCandidateBasket, PortfolioBasketItem
from .common import status_from_blockers, to_plain


@dataclass(frozen=True)
class AllocationConstraints:
    max_allocation_per_symbol: float = 0.45
    min_allocation_per_item: float = 0.0
    max_symbols: int = 10
    max_strategies: int = 6
    max_model_aliases: int = 6
    min_data_quality_score: float = 0.0
    risk_budget_cap: float = 1.0
    total_tolerance: float = 0.0001
    max_warning_candidates: int = 0
    rebalance_frequency: str = "paper_daily"


@dataclass(frozen=True)
class AllocationConstraintViolation:
    code: str
    message: str
    severity: str = "block"


@dataclass(frozen=True)
class AllocationConstraintReport:
    status: str
    violations: list[AllocationConstraintViolation]
    warnings: list[str]
    constraints: AllocationConstraints
    live_trading_enabled: bool = False


def validate_allocation(
    basket: PortfolioCandidateBasket,
    weights: dict[str, float],
    constraints: AllocationConstraints | None = None,
) -> dict[str, Any]:
    constraints = constraints or AllocationConstraints()
    violations: list[AllocationConstraintViolation] = []
    warnings: list[str] = []
    total = sum(float(value) for value in weights.values())
    if abs(total - 1.0) > constraints.total_tolerance:
        violations.append(AllocationConstraintViolation("total_allocation", "paper allocation weights must sum to 1.0"))
    items_by_id: dict[str, PortfolioBasketItem] = {item.item_id: item for item in basket.items}
    active_items = [items_by_id[item_id] for item_id in weights if item_id in items_by_id and weights[item_id] > 0]
    if len({item.symbol for item in active_items}) > constraints.max_symbols:
        violations.append(AllocationConstraintViolation("max_symbols", "too many symbols for portfolio research constraints"))
    if len({item.strategy_id for item in active_items}) > constraints.max_strategies:
        violations.append(AllocationConstraintViolation("max_strategies", "too many strategies for portfolio research constraints"))
    if len({item.model_alias for item in active_items}) > constraints.max_model_aliases:
        violations.append(AllocationConstraintViolation("max_models", "too many model aliases for portfolio research constraints"))
    symbol_weights: dict[str, float] = {}
    warning_candidates = 0
    for item_id, weight in weights.items():
        item = items_by_id.get(item_id)
        if item is None:
            violations.append(AllocationConstraintViolation("unknown_item", f"unknown allocation item {item_id}"))
            continue
        if item.disabled or item.blocked_reason:
            violations.append(AllocationConstraintViolation("blocked_candidate", f"blocked candidate cannot be active: {item_id}"))
        if weight > 0 and weight < constraints.min_allocation_per_item:
            violations.append(AllocationConstraintViolation("min_item", f"allocation below minimum for {item_id}"))
        if item.data_quality_score < constraints.min_data_quality_score:
            violations.append(AllocationConstraintViolation("data_quality", f"data quality below minimum for {item_id}"))
        if item.warnings:
            warning_candidates += 1
        symbol_weights[item.symbol] = symbol_weights.get(item.symbol, 0.0) + float(weight)
    for symbol, weight in symbol_weights.items():
        if weight > constraints.max_allocation_per_symbol:
            violations.append(AllocationConstraintViolation("symbol_exposure", f"{symbol} exceeds max paper exposure"))
    if warning_candidates > constraints.max_warning_candidates:
        warnings.append("basket contains warning candidates")
    return to_plain(AllocationConstraintReport(status_from_blockers([v.message for v in violations], warnings), violations, warnings, constraints))


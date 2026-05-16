from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT, PAPER_ONLY_RESEARCH_STATEMENT
from .allocation_constraints import AllocationConstraints, validate_allocation
from .candidate_basket import PortfolioCandidateBasket
from .common import has_advice_wording, now_ms, stable_hash, status_from_blockers, to_plain


@dataclass(frozen=True)
class PortfolioAllocationItem:
    item_id: str
    symbol: str
    weight: float
    paper_only: bool = True
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class PortfolioAllocationProposal:
    allocation_id: str
    basket_id: str
    mode: str
    items: list[PortfolioAllocationItem]
    created_at_ms: int
    no_live_statement: str = NO_LIVE_STATEMENT
    no_financial_advice_statement: str = NO_ADVICE_STATEMENT
    paper_only_research_statement: str = PAPER_ONLY_RESEARCH_STATEMENT
    live_trading_enabled: bool = False


def propose_allocation(
    basket: PortfolioCandidateBasket,
    *,
    mode: str = "equal_weight",
    constraints: AllocationConstraints | None = None,
) -> dict[str, Any]:
    active = [item for item in basket.items if not item.disabled and not item.blocked_reason]
    raw: dict[str, float] = {}
    if not active:
        raw = {}
    elif mode == "equal_weight":
        raw = {item.item_id: 1.0 for item in active}
    elif mode == "score_weighted":
        raw = {item.item_id: max(0.01, item.paper_score) for item in active}
    elif mode == "inverse_drawdown_weighted":
        raw = {item.item_id: 1.0 / max(0.005, abs(item.max_drawdown)) for item in active}
    elif mode == "inverse_volatility_weighted":
        buckets = {"low": 3.0, "medium": 2.0, "high": 1.0}
        raw = {item.item_id: buckets.get(item.volatility_bucket, 1.5) for item in active}
    elif mode in {"liquidity_adjusted", "risk_budget_balanced", "conservative_research"}:
        raw = {item.item_id: max(0.01, item.data_quality_score + item.market_quality_score - abs(item.max_drawdown) * 100.0) for item in active}
    else:
        raw = {item.item_id: 1.0 for item in active}
    total = sum(raw.values()) or 1.0
    weights = {item_id: value / total for item_id, value in raw.items()}
    allocation = PortfolioAllocationProposal(
        allocation_id=f"allocation-{stable_hash({'basket_id': basket.basket_id, 'mode': mode, 'weights': weights})[:12]}",
        basket_id=basket.basket_id,
        mode=mode,
        items=[PortfolioAllocationItem(item.item_id, item.symbol, round(weights.get(item.item_id, 0.0), 8)) for item in active],
        created_at_ms=now_ms(),
    )
    payload = to_plain(allocation)
    constraint_report = validate_allocation(basket, {item["item_id"]: float(item["weight"]) for item in payload["items"]}, constraints)
    blockers = list(constraint_report.get("violations", []))
    if has_advice_wording(payload):
        blockers.append({"code": "advice_wording", "message": "advice wording blocked", "severity": "block"})
    return {
        "status": status_from_blockers([str(item) for item in blockers], constraint_report.get("warnings", [])),
        "proposal": payload,
        "constraint_report": constraint_report,
        "blockers": blockers,
        "warnings": constraint_report.get("warnings", []),
        "live_trading_enabled": False,
    }


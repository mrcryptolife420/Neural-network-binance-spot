from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT, PAPER_ONLY_RESEARCH_STATEMENT
from .common import has_advice_wording, json_write, now_ms, redact_value, stable_hash, status_from_blockers, to_plain


@dataclass(frozen=True)
class PortfolioBasketItem:
    item_id: str
    symbol: str
    strategy_id: str
    model_alias: str
    risk_preset: str
    source_candidate_id: str
    source_scorecard_id: str
    paper_score: float
    data_quality_score: float
    market_quality_score: float
    warnings: list[str] = field(default_factory=list)
    blocked_reason: str | None = None
    disabled: bool = False
    volatility_bucket: str = "medium"
    max_drawdown: float = 0.0
    block_rate: float = 0.0
    trades: int = 0
    paper_only: bool = True
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class PortfolioBasketSource:
    source_type: str = "strategy_lab_scorecards"
    source_id: str = "fixture"
    source_path: str = ""
    source_hash: str = ""


@dataclass(frozen=True)
class PortfolioCandidateBasket:
    basket_id: str
    name: str
    description: str
    source_queue_id: str
    source_scanner_run_id: str
    items: list[PortfolioBasketItem]
    max_items: int = 10
    quote_asset: str = "USDT"
    created_at_ms: int = field(default_factory=now_ms)
    source: PortfolioBasketSource = field(default_factory=PortfolioBasketSource)
    no_live_statement: str = NO_LIVE_STATEMENT
    no_financial_advice_statement: str = NO_ADVICE_STATEMENT
    paper_only_research_statement: str = PAPER_ONLY_RESEARCH_STATEMENT
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class PortfolioBasketValidationResult:
    status: str
    blockers: list[str]
    warnings: list[str]
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class PortfolioBasketBuildReport:
    status: str
    basket: PortfolioCandidateBasket
    validation: PortfolioBasketValidationResult
    item_count: int
    active_item_count: int
    basket_hash: str
    live_trading_enabled: bool = False


def portfolio_candidate_basket_to_dict(basket: PortfolioCandidateBasket) -> dict[str, Any]:
    return redact_value(to_plain(basket))


def validate_portfolio_candidate_basket(basket: PortfolioCandidateBasket) -> PortfolioBasketValidationResult:
    blockers: list[str] = []
    warnings: list[str] = []
    if basket.live_trading_enabled:
        blockers.append("basket live_trading_enabled must be false")
    if not basket.no_live_statement:
        blockers.append("missing no_live_statement")
    if not basket.no_financial_advice_statement:
        blockers.append("missing no_financial_advice_statement")
    if not basket.paper_only_research_statement:
        blockers.append("missing paper_only_research_statement")
    if len(basket.items) > basket.max_items:
        blockers.append("max_items exceeded")
    seen_items: set[str] = set()
    seen_active_combos: set[tuple[str, str, str, str]] = set()
    for item in basket.items:
        if item.item_id in seen_items:
            blockers.append(f"duplicate item_id: {item.item_id}")
        seen_items.add(item.item_id)
        if item.live_trading_enabled:
            blockers.append(f"item live_trading_enabled must be false: {item.item_id}")
        if not item.paper_only:
            blockers.append(f"item paper_only must be true: {item.item_id}")
        if item.blocked_reason and not item.disabled:
            blockers.append(f"blocked item must be disabled: {item.item_id}")
        if min(item.paper_score, item.data_quality_score, item.market_quality_score) < 0:
            blockers.append(f"negative score blocked: {item.item_id}")
        combo = (item.symbol.upper(), item.strategy_id, item.model_alias, item.risk_preset)
        if not item.disabled and not item.blocked_reason:
            if combo in seen_active_combos:
                blockers.append(f"duplicate active combo: {item.symbol}/{item.strategy_id}/{item.model_alias}/{item.risk_preset}")
            seen_active_combos.add(combo)
    safe_payload = portfolio_candidate_basket_to_dict(basket)
    if has_advice_wording(safe_payload):
        blockers.append("advice wording blocked")
    return PortfolioBasketValidationResult(status_from_blockers(blockers, warnings), blockers, warnings)


def build_report(basket: PortfolioCandidateBasket) -> dict[str, Any]:
    validation = validate_portfolio_candidate_basket(basket)
    report = PortfolioBasketBuildReport(
        status=validation.status,
        basket=basket,
        validation=validation,
        item_count=len(basket.items),
        active_item_count=len([item for item in basket.items if not item.disabled and not item.blocked_reason]),
        basket_hash=stable_hash(basket),
    )
    return redact_value(to_plain(report))


def basket_from_scorecards(scorecards: list[dict[str, Any]], *, max_items: int = 6, name: str = "Portfolio Research Basket") -> PortfolioCandidateBasket:
    items: list[PortfolioBasketItem] = []
    for index, card in enumerate(scorecards[:max_items]):
        symbol = str(card.get("symbol") or card.get("candidate", {}).get("symbol") or f"SYMBOL{index}USDT").upper()
        item_id = f"basket-item-{index + 1}-{symbol.lower()}"
        paper_score = float(card.get("score") or card.get("paper_score") or max(1.0, 100.0 - index * 8.0))
        drawdown = abs(float(card.get("max_drawdown") or card.get("drawdown") or (index + 1) * 0.01))
        items.append(
            PortfolioBasketItem(
                item_id=item_id,
                symbol=symbol,
                strategy_id=str(card.get("strategy_id") or "rule_baseline"),
                model_alias=str(card.get("model_alias") or "tiny_nn_v1"),
                risk_preset=str(card.get("risk_preset") or "conservative"),
                source_candidate_id=str(card.get("candidate_id") or item_id),
                source_scorecard_id=str(card.get("scorecard_id") or f"scorecard-{index + 1}"),
                paper_score=paper_score,
                data_quality_score=float(card.get("data_quality_score") or 90.0 - index),
                market_quality_score=float(card.get("market_quality_score") or 88.0 - index),
                warnings=list(card.get("warnings") or []),
                blocked_reason=card.get("blocked_reason"),
                disabled=bool(card.get("blocked_reason")),
                volatility_bucket=str(card.get("volatility_bucket") or ("low" if index % 3 == 0 else "medium")),
                max_drawdown=drawdown,
                block_rate=float(card.get("block_rate") or 0.0),
                trades=int(card.get("trades") or 12 + index),
            )
        )
    return PortfolioCandidateBasket(
        basket_id=f"basket-{stable_hash([to_plain(item) for item in items])[:12]}",
        name=name,
        description="Local paper-only portfolio research basket from Strategy Lab scorecards.",
        source_queue_id="latest",
        source_scanner_run_id="latest",
        items=items,
        max_items=max_items,
    )


def fixture_basket(max_items: int = 4) -> PortfolioCandidateBasket:
    scorecards = [
        {"symbol": "BTCUSDT", "score": 91, "max_drawdown": 0.025, "trades": 18},
        {"symbol": "ETHUSDT", "score": 86, "max_drawdown": 0.032, "trades": 17},
        {"symbol": "BNBUSDT", "score": 79, "max_drawdown": 0.041, "trades": 14},
        {"symbol": "SOLUSDT", "score": 74, "max_drawdown": 0.055, "trades": 13},
    ]
    return basket_from_scorecards(scorecards, max_items=max_items)


def write_portfolio_candidate_basket(root: Path, basket: PortfolioCandidateBasket) -> dict[str, Any]:
    payload = build_report(basket)
    path = root / "data" / "portfolio-lab" / "baskets" / basket.basket_id / "basket.json"
    saved = json_write(path, payload)
    payload["saved"] = saved
    return payload


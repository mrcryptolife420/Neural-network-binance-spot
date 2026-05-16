from __future__ import annotations

from typing import Any

from .candidate_basket import PortfolioCandidateBasket, basket_from_scorecards, build_report, fixture_basket


def build_candidate_basket(
    scorecards: list[dict[str, Any]] | None = None,
    *,
    mode: str = "top_score",
    max_items: int = 6,
    min_paper_score: float = 0.0,
    min_data_quality_score: float = 0.0,
    max_drawdown: float = 1.0,
    quote_asset: str = "USDT",
    include_symbols: list[str] | None = None,
    exclude_symbols: list[str] | None = None,
    require_research_guard_pass: bool = False,
) -> dict[str, Any]:
    if scorecards:
        rows = list(scorecards)
    else:
        rows = [item.__dict__ for item in fixture_basket(max_items=max_items).items]
    include = {item.upper() for item in include_symbols or []}
    exclude = {item.upper() for item in exclude_symbols or []}
    filtered: list[dict[str, Any]] = []
    warnings: list[str] = []
    for row in rows:
        symbol = str(row.get("symbol", "")).upper()
        if quote_asset and not symbol.endswith(quote_asset.upper()):
            continue
        if include and symbol not in include:
            continue
        if exclude and symbol in exclude:
            continue
        if float(row.get("paper_score") or row.get("score") or 0.0) < min_paper_score:
            continue
        if float(row.get("data_quality_score") or 100.0) < min_data_quality_score:
            continue
        if abs(float(row.get("max_drawdown") or row.get("drawdown") or 0.0)) > max_drawdown:
            continue
        if require_research_guard_pass and str(row.get("guard_status", "pass")) not in {"pass", "ok"}:
            continue
        filtered.append(row)
    if mode in {"top_score", "high_volume"}:
        filtered.sort(key=lambda item: float(item.get("paper_score") or item.get("score") or 0.0), reverse=True)
    elif mode in {"conservative", "low_drawdown"}:
        filtered.sort(key=lambda item: (abs(float(item.get("max_drawdown") or item.get("drawdown") or 0.0)), -float(item.get("paper_score") or item.get("score") or 0.0)))
    elif mode in {"diversified", "model_balanced", "strategy_balanced"}:
        filtered.sort(key=lambda item: (str(item.get("strategy_id") or ""), str(item.get("model_alias") or ""), -float(item.get("paper_score") or item.get("score") or 0.0)))
    elif mode != "custom":
        warnings.append(f"unknown mode used as custom: {mode}")
    basket: PortfolioCandidateBasket = basket_from_scorecards(filtered[:max_items], max_items=max_items, name=f"{mode} portfolio research basket")
    payload = build_report(basket)
    payload["build_mode"] = mode
    payload["filters"] = {
        "max_items": max_items,
        "min_paper_score": min_paper_score,
        "min_data_quality_score": min_data_quality_score,
        "max_drawdown": max_drawdown,
        "quote_asset": quote_asset,
    }
    payload["warnings"] = list(payload.get("warnings", [])) + warnings
    payload["live_trading_enabled"] = False
    return payload


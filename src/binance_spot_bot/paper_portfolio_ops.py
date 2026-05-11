from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any

from .config import BotSettings
from .portfolio import Portfolio
from .redaction import redact_payload


@dataclass(frozen=True)
class PaperStrategy:
    strategy_id: str
    score: float
    symbols: list[str]
    max_weight: Decimal = Decimal("0.40")
    status: str = "paper_approved"


@dataclass(frozen=True)
class PaperPortfolioPlan:
    portfolio_id: str
    total_quote_budget: Decimal
    allocations: list[dict[str, Any]]
    conflicts: list[dict[str, Any]]
    risk_limits: dict[str, Any]
    rotation: list[dict[str, Any]]
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def build_portfolio_allocation(strategies: list[PaperStrategy], total_quote_budget: Decimal) -> PaperPortfolioPlan:
    approved = [item for item in strategies if item.status == "paper_approved" and item.score > 0]
    total_score = sum(item.score for item in approved) or 1.0
    allocations = []
    symbol_owner: dict[str, tuple[str, float]] = {}
    conflicts = []
    for strategy in sorted(approved, key=lambda item: item.score, reverse=True):
        raw_weight = Decimal(str(strategy.score / total_score))
        weight = min(strategy.max_weight, raw_weight)
        quote = (total_quote_budget * weight).quantize(Decimal("0.01"))
        for symbol in strategy.symbols:
            normalized = symbol.upper()
            previous = symbol_owner.get(normalized)
            if previous:
                winner = strategy.strategy_id if strategy.score > previous[1] else previous[0]
                conflicts.append({"symbol": normalized, "strategies": [previous[0], strategy.strategy_id], "winner": winner})
                if winner != strategy.strategy_id:
                    continue
            symbol_owner[normalized] = (strategy.strategy_id, strategy.score)
            allocations.append(
                {
                    "strategy_id": strategy.strategy_id,
                    "symbol": normalized,
                    "weight": str(weight),
                    "quote_budget": str(quote),
                    "max_open_orders": 2,
                }
            )
    rotation = [
        {
            "strategy_id": item.strategy_id,
            "action": "eligible" if item.score >= 0.60 else "watch",
            "reason": "score_above_threshold" if item.score >= 0.60 else "score_below_threshold",
        }
        for item in approved
    ]
    return PaperPortfolioPlan(
        portfolio_id=f"paper-portfolio-{int(time.time() * 1000)}",
        total_quote_budget=total_quote_budget,
        allocations=allocations,
        conflicts=conflicts,
        risk_limits={
            "max_total_exposure_quote": str(total_quote_budget),
            "max_strategy_weight": "0.40",
            "max_open_positions": max(1, len({row["symbol"] for row in allocations})),
            "max_daily_loss_quote": str((total_quote_budget * Decimal("0.05")).quantize(Decimal("0.01"))),
        },
        rotation=rotation,
    )


def portfolio_attribution(fills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    totals: dict[str, Decimal] = {}
    trades: dict[str, int] = {}
    for fill in fills:
        strategy = str(fill.get("strategy_id", "unknown"))
        totals[strategy] = totals.get(strategy, Decimal("0")) + Decimal(str(fill.get("pnl", "0")))
        trades[strategy] = trades.get(strategy, 0) + 1
    return [
        {"strategy_id": strategy, "pnl": str(pnl), "trades": trades[strategy]}
        for strategy, pnl in sorted(totals.items())
    ]


def portfolio_watchdog(plan: PaperPortfolioPlan, portfolio: Portfolio, marks: dict[str, Decimal]) -> dict[str, Any]:
    equity = portfolio.total_equity(marks)
    exposure = portfolio.total_exposure(marks)
    max_exposure = Decimal(str(plan.risk_limits["max_total_exposure_quote"]))
    max_loss = Decimal(str(plan.risk_limits["max_daily_loss_quote"]))
    loss = max(Decimal("0"), plan.total_quote_budget - equity)
    blockers = []
    if exposure > max_exposure:
        blockers.append("portfolio_exposure_limit")
    if loss > max_loss:
        blockers.append("portfolio_daily_loss_limit")
    return {
        "status": "blocked" if blockers else "healthy",
        "equity": str(equity),
        "exposure": str(exposure),
        "loss": str(loss),
        "blockers": blockers,
        "live_trading_enabled": False,
    }


def rotate_strategies(plan: PaperPortfolioPlan, attribution: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pnl_by_strategy = {row["strategy_id"]: Decimal(str(row.get("pnl", "0"))) for row in attribution}
    rows = []
    for row in plan.rotation:
        strategy = row["strategy_id"]
        pnl = pnl_by_strategy.get(strategy, Decimal("0"))
        action = "pause" if pnl < Decimal("-5") else row["action"]
        rows.append({"strategy_id": strategy, "pnl": str(pnl), "action": action, "guardrail": "paper_only"})
    return rows


def write_portfolio_evidence(settings: BotSettings, plan: PaperPortfolioPlan, watchdog: dict[str, Any], attribution: list[dict[str, Any]]) -> dict[str, str]:
    out = settings.data_dir / "paper-portfolio"
    out.mkdir(parents=True, exist_ok=True)
    payload = {"plan": plan.to_dict(), "watchdog": watchdog, "attribution": attribution, "live_trading_enabled": False}
    json_path = out / f"{plan.portfolio_id}.json"
    latest_path = out / "latest.json"
    md_path = out / "portfolio-report.md"
    json_path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    latest_path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Paper Portfolio Report",
                "",
                f"Portfolio: {plan.portfolio_id}",
                f"Status: {watchdog.get('status')}",
                f"Allocations: {len(plan.allocations)}",
                f"Conflicts: {len(plan.conflicts)}",
                "Live trading: disabled",
            ]
        ),
        encoding="utf-8",
    )
    return {"json": str(json_path), "latest": str(latest_path), "markdown": str(md_path)}


def run_portfolio_operations(settings: BotSettings, strategies: list[PaperStrategy], total_quote_budget: Decimal, fills: list[dict[str, Any]]) -> dict[str, Any]:
    plan = build_portfolio_allocation(strategies, total_quote_budget)
    portfolio = Portfolio()
    portfolio.set_balance("USDT", total_quote_budget)
    marks = {row["symbol"]: Decimal("100") for row in plan.allocations}
    attribution = portfolio_attribution(fills)
    watchdog = portfolio_watchdog(plan, portfolio, marks)
    rotation = rotate_strategies(plan, attribution)
    evidence = write_portfolio_evidence(settings, plan, watchdog, attribution)
    return {"plan": plan.to_dict(), "watchdog": watchdog, "attribution": attribution, "rotation": rotation, "evidence": evidence}

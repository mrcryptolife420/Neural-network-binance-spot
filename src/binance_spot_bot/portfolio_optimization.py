from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from .config import BotSettings
from .paper_portfolio_ops import PaperPortfolioPlan
from .portfolio_benchmarking import StressScenario, benchmark_allocations
from .redaction import redact_payload


@dataclass(frozen=True)
class RiskBudgetCandidate:
    name: str
    max_strategy_weight: Decimal
    max_daily_loss_pct: Decimal
    rotation_threshold: float


@dataclass(frozen=True)
class PolicyCard:
    policy_id: str
    selected_candidate: str
    robustness_score: float
    max_strategy_weight: Decimal
    max_daily_loss_pct: Decimal
    rotation_threshold: float
    status: str
    selection_reason: str
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


DEFAULT_CANDIDATES = [
    RiskBudgetCandidate("conservative", Decimal("0.25"), Decimal("0.03"), 0.65),
    RiskBudgetCandidate("balanced", Decimal("0.35"), Decimal("0.05"), 0.60),
    RiskBudgetCandidate("aggressive-paper", Decimal("0.45"), Decimal("0.08"), 0.55),
]


def search_risk_budgets(plan: PaperPortfolioPlan, scenarios: list[StressScenario] | None = None) -> list[dict[str, Any]]:
    rows = []
    for candidate in DEFAULT_CANDIDATES:
        adjusted = PaperPortfolioPlan(
            portfolio_id=plan.portfolio_id,
            total_quote_budget=plan.total_quote_budget,
            allocations=[_cap_allocation(row, candidate.max_strategy_weight, plan.total_quote_budget) for row in plan.allocations],
            conflicts=plan.conflicts,
            risk_limits={
                **plan.risk_limits,
                "max_strategy_weight": str(candidate.max_strategy_weight),
                "max_daily_loss_quote": str((plan.total_quote_budget * candidate.max_daily_loss_pct).quantize(Decimal("0.01"))),
            },
            rotation=plan.rotation,
        )
        benchmark = benchmark_allocations(adjusted, scenarios)
        rows.append(
            {
                "candidate": candidate.name,
                "robustness_score": benchmark["robustness_score"],
                "benchmark_status": benchmark["status"],
                "max_strategy_weight": str(candidate.max_strategy_weight),
                "max_daily_loss_pct": str(candidate.max_daily_loss_pct),
                "rotation_threshold": candidate.rotation_threshold,
            }
        )
    return sorted(rows, key=lambda row: (row["benchmark_status"] == "pass", row["robustness_score"]), reverse=True)


def select_robust_policy(plan: PaperPortfolioPlan, search_rows: list[dict[str, Any]]) -> PolicyCard:
    passing = [row for row in search_rows if row["benchmark_status"] == "pass"] or search_rows
    conservative_order = {"conservative": 0, "balanced": 1, "aggressive-paper": 2}
    selected = sorted(passing, key=lambda row: (-float(row["robustness_score"]), conservative_order.get(row["candidate"], 99)))[0]
    return PolicyCard(
        policy_id=f"policy-{int(time.time() * 1000)}",
        selected_candidate=selected["candidate"],
        robustness_score=float(selected["robustness_score"]),
        max_strategy_weight=Decimal(str(selected["max_strategy_weight"])),
        max_daily_loss_pct=Decimal(str(selected["max_daily_loss_pct"])),
        rotation_threshold=float(selected["rotation_threshold"]),
        status="paper_selected",
        selection_reason="stress_pass_then_highest_robustness_with_conservative_tiebreak",
    )


def write_policy_card(settings: BotSettings, card: PolicyCard, search_rows: list[dict[str, Any]]) -> dict[str, str]:
    out = settings.data_dir / "paper-portfolio" / "policies"
    out.mkdir(parents=True, exist_ok=True)
    payload = {"policy": card.to_dict(), "search": search_rows, "live_trading_enabled": False}
    latest = out / "latest-policy-card.json"
    stamped = out / f"{card.policy_id}.json"
    md = out / "policy-card.md"
    latest.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    stamped.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    md.write_text(
        "\n".join(
            [
                "# Paper Portfolio Policy Card",
                "",
                f"Policy: {card.policy_id}",
                f"Selected: {card.selected_candidate}",
                f"Robustness: {card.robustness_score}",
                f"Reason: {card.selection_reason}",
                "Live trading: disabled",
            ]
        ),
        encoding="utf-8",
    )
    return {"latest": str(latest), "json": str(stamped), "markdown": str(md)}


def optimize_portfolio_policy(settings: BotSettings, plan: PaperPortfolioPlan) -> dict[str, Any]:
    search = search_risk_budgets(plan)
    card = select_robust_policy(plan, search)
    paths = write_policy_card(settings, card, search)
    return {"policy": card.to_dict(), "search": search, "paths": paths}


def _cap_allocation(row: dict[str, Any], cap: Decimal, total_budget: Decimal) -> dict[str, Any]:
    capped = dict(row)
    max_quote = (total_budget * cap).quantize(Decimal("0.01"))
    quote = Decimal(str(row.get("quote_budget", "0")))
    capped["quote_budget"] = str(min(quote, max_quote))
    capped["weight"] = str(cap)
    return capped

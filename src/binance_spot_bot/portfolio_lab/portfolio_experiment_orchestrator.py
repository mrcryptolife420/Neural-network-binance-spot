from __future__ import annotations

from pathlib import Path
from typing import Any

from . import NO_LIVE_STATEMENT, PAPER_ONLY_RESEARCH_STATEMENT, PAPER_PORTFOLIO_CONFIRM
from .allocation_proposals import propose_allocation
from .allocation_scorecards import build_allocation_scorecards
from .basket_builder import build_candidate_basket
from .basket_simulation import simulate_basket
from .candidate_basket import PortfolioCandidateBasket, build_report, fixture_basket
from .common import json_write, now_ms, stable_hash
from .correlation_proxy import portfolio_correlation_proxy
from .portfolio_research_guards import evaluate_portfolio_research_guards
from .portfolio_risk_analytics import analyze_portfolio_risk
from .stress_tests import run_portfolio_stress_tests


def preview_portfolio_simulation(basket: PortfolioCandidateBasket | None = None, allocation: dict[str, Any] | None = None) -> dict[str, Any]:
    basket = basket or fixture_basket()
    allocation = allocation or propose_allocation(basket)["proposal"]
    return {
        "status": "ok",
        "preview_id": f"portfolio-preview-{stable_hash({'basket': basket.basket_id, 'allocation': allocation.get('allocation_id')})[:12]}",
        "basket": build_report(basket),
        "allocation": allocation,
        "estimated_steps": 48,
        "requires_confirm": PAPER_PORTFOLIO_CONFIRM,
        "live_trading_enabled": False,
    }


def run_portfolio_experiment(
    root: Path,
    *,
    basket: PortfolioCandidateBasket | None = None,
    allocation: dict[str, Any] | None = None,
    confirm: str = "",
) -> dict[str, Any]:
    if confirm != PAPER_PORTFOLIO_CONFIRM:
        return {"status": "blocked", "blockers": [f"portfolio experiment requires confirm {PAPER_PORTFOLIO_CONFIRM}"], "live_trading_enabled": False}
    basket = basket or fixture_basket()
    allocation = allocation or propose_allocation(basket)["proposal"]
    simulation = simulate_basket(basket, allocation)
    risk = analyze_portfolio_risk(basket, allocation, simulation)
    correlation = portfolio_correlation_proxy(basket)
    stress = run_portfolio_stress_tests(simulation)
    guards = evaluate_portfolio_research_guards(basket, allocation, risk, stress, correlation)
    scorecards = build_allocation_scorecards(risk, stress, guards)
    run_id = f"portfolio-run-{stable_hash({'basket': basket.basket_id, 'allocation': allocation.get('allocation_id'), 'ts': now_ms()})[:12]}"
    report = {
        "status": "completed" if guards["status"] != "blocked" else "blocked",
        "run_id": run_id,
        "basket_id": basket.basket_id,
        "allocation_id": allocation.get("allocation_id"),
        "mode": "paper",
        "start_ms": now_ms(),
        "end_ms": now_ms(),
        "rebalance_policy": "paper_static",
        "no_live_statement": NO_LIVE_STATEMENT,
        "paper_only_research_statement": PAPER_ONLY_RESEARCH_STATEMENT,
        "basket": build_report(basket),
        "allocation": allocation,
        "simulation": simulation,
        "risk": risk,
        "correlation": correlation,
        "stress": stress,
        "guards": guards,
        "scorecards": scorecards,
        "live_trading_enabled": False,
    }
    saved = json_write(root / "data" / "portfolio-lab" / "runs" / run_id / "portfolio-run.json", report)
    report["saved"] = saved
    return report


def build_default_portfolio_lab_flow(root: Path) -> dict[str, Any]:
    basket_payload = build_candidate_basket(mode="top_score", max_items=4)
    basket = fixture_basket(max_items=4)
    allocation_payload = propose_allocation(basket, mode="equal_weight")
    run = run_portfolio_experiment(root, basket=basket, allocation=allocation_payload["proposal"], confirm=PAPER_PORTFOLIO_CONFIRM)
    return {"status": "ok", "basket": basket_payload, "allocation": allocation_payload, "run": run, "live_trading_enabled": False}


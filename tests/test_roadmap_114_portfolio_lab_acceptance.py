from __future__ import annotations

from dataclasses import replace

from binance_spot_bot.portfolio_lab import PAPER_PORTFOLIO_CONFIRM, portfolio_lab_health
from binance_spot_bot.portfolio_lab.allocation_constraints import validate_allocation
from binance_spot_bot.portfolio_lab.allocation_proposals import propose_allocation
from binance_spot_bot.portfolio_lab.basket_builder import build_candidate_basket
from binance_spot_bot.portfolio_lab.candidate_basket import (
    PortfolioBasketItem,
    PortfolioCandidateBasket,
    fixture_basket,
    portfolio_candidate_basket_to_dict,
    validate_portfolio_candidate_basket,
)
from binance_spot_bot.portfolio_lab.correlation_proxy import portfolio_correlation_proxy
from binance_spot_bot.portfolio_lab.evidence_bundle import export_portfolio_lab_evidence
from binance_spot_bot.portfolio_lab.portfolio_experiment_orchestrator import preview_portfolio_simulation, run_portfolio_experiment
from binance_spot_bot.portfolio_lab.portfolio_research_guards import evaluate_portfolio_research_guards


def test_dashboard_v2_portfolio_lab_api_smoke() -> None:
    try:
        from fastapi.testclient import TestClient
    except Exception:
        return
    from binance_spot_bot.dashboard_v2.app import create_dashboard_v2_app

    client = TestClient(create_dashboard_v2_app())
    assert client.get("/api/portfolio-lab/health").json()["live_trading_enabled"] is False
    assert client.post("/api/portfolio-lab/baskets/build").json()["status"] == "ok"
    assert client.post("/api/portfolio-lab/simulations/run").json()["status"] == "blocked"


def test_portfolio_lab_safety_contract_and_basket_validation() -> None:
    health = portfolio_lab_health()
    assert health["status"] == "ok"
    assert health["live_trading_enabled"] is False
    assert health["requires_api_keys"] is False
    basket = fixture_basket()
    validation = validate_portfolio_candidate_basket(basket)
    assert validation.status == "ok"
    assert portfolio_candidate_basket_to_dict(basket)["live_trading_enabled"] is False


def test_portfolio_basket_blocks_live_duplicates_negative_scores_and_wording() -> None:
    basket = fixture_basket()
    live = replace(basket, live_trading_enabled=True)
    assert validate_portfolio_candidate_basket(live).status == "blocked"
    duplicate = replace(basket, items=[basket.items[0], basket.items[0]])
    assert validate_portfolio_candidate_basket(duplicate).status == "blocked"
    negative_item = replace(basket.items[0], item_id="negative", paper_score=-1)
    negative = replace(basket, items=[negative_item])
    assert validate_portfolio_candidate_basket(negative).status == "blocked"
    unsafe = replace(basket, description="direct buy wording")
    assert validate_portfolio_candidate_basket(unsafe).status == "blocked"


def test_blocked_candidate_must_be_disabled() -> None:
    item = PortfolioBasketItem(
        item_id="blocked",
        symbol="BTCUSDT",
        strategy_id="rule_baseline",
        model_alias="tiny_nn_v1",
        risk_preset="conservative",
        source_candidate_id="c1",
        source_scorecard_id="s1",
        paper_score=10,
        data_quality_score=10,
        market_quality_score=10,
        blocked_reason="guard",
        disabled=False,
    )
    basket = PortfolioCandidateBasket("b1", "blocked basket", "paper research", "q1", "scan1", [item])
    assert validate_portfolio_candidate_basket(basket).status == "blocked"


def test_builder_allocation_constraints_and_preview_are_paper_only() -> None:
    basket_payload = build_candidate_basket(mode="top_score", max_items=3)
    assert basket_payload["status"] == "ok"
    basket = fixture_basket(max_items=3)
    proposal = propose_allocation(basket, mode="equal_weight")
    assert proposal["status"] == "ok"
    weights = {item["item_id"]: float(item["weight"]) for item in proposal["proposal"]["items"]}
    assert validate_allocation(basket, weights)["status"] == "ok"
    preview = preview_portfolio_simulation(basket, proposal["proposal"])
    assert preview["live_trading_enabled"] is False
    assert preview["requires_confirm"] == PAPER_PORTFOLIO_CONFIRM


def test_simulation_confirm_gate_risk_stress_scorecards_guards_and_evidence(tmp_path) -> None:
    blocked = run_portfolio_experiment(tmp_path, confirm="")
    assert blocked["status"] == "blocked"
    basket = fixture_basket()
    proposal = propose_allocation(basket)["proposal"]
    run = run_portfolio_experiment(tmp_path, basket=basket, allocation=proposal, confirm=PAPER_PORTFOLIO_CONFIRM)
    assert run["live_trading_enabled"] is False
    assert run["simulation"]["equity_curve"]
    assert run["risk"]["live_trading_enabled"] is False
    assert run["stress"]["live_trading_enabled"] is False
    assert run["scorecards"]["scorecards"][0]["summary"] == "candidate allocation for paper research only"
    guards = evaluate_portfolio_research_guards(basket, proposal, run["risk"], run["stress"], portfolio_correlation_proxy(basket))
    assert guards["status"] in {"pass", "warn"}
    evidence = export_portfolio_lab_evidence(tmp_path, run)
    assert evidence["status"] == "ok"
    assert evidence["manifest"]["redaction_proof"] is True

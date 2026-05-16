from __future__ import annotations

from binance_spot_bot.portfolio_lab import WALK_FORWARD_CONFIRM
from binance_spot_bot.portfolio_lab.allocation_decay import analyze_allocation_decay
from binance_spot_bot.portfolio_lab.allocation_proposals import propose_allocation
from binance_spot_bot.portfolio_lab.allocation_robustness_scorecards import build_robustness_scorecards
from binance_spot_bot.portfolio_lab.candidate_basket import fixture_basket
from binance_spot_bot.portfolio_lab.candidate_replacement import simulate_candidate_replacements
from binance_spot_bot.portfolio_lab.dataset_coverage_audit import audit_dataset_coverage
from binance_spot_bot.portfolio_lab.rebalance_event_simulator import simulate_rebalance_events
from binance_spot_bot.portfolio_lab.rebalancing_schedules import default_rebalancing_schedules, validate_rebalancing_schedule
from binance_spot_bot.portfolio_lab.robustness_governance_gate import evaluate_robustness_governance_gate
from binance_spot_bot.portfolio_lab.rolling_portfolio_orchestrator import preview_rolling_portfolio_simulation, run_rolling_portfolio_simulation
from binance_spot_bot.portfolio_lab.walk_forward_evidence_bundle import export_walk_forward_evidence
from binance_spot_bot.portfolio_lab.walk_forward_performance import analyze_walk_forward_performance
from binance_spot_bot.portfolio_lab.walk_forward_splits import WalkForwardSplit, build_walk_forward_split, validate_walk_forward_split


def test_walk_forward_split_validation_blocks_unsafe_boundaries_and_wording() -> None:
    split_payload = build_walk_forward_split()
    assert split_payload["status"] == "ok"
    split = WalkForwardSplit(
        split_id="unsafe",
        mode="rolling_window",
        windows=[],
        symbols=["BTCUSDT"],
        live_trading_enabled=True,
        no_financial_advice_statement="",
        paper_only_research_statement="direct buy wording",
    )
    validation = validate_walk_forward_split(split)
    assert validation.status == "blocked"
    assert any("empty windows" in blocker for blocker in validation.blockers)


def test_dataset_coverage_schedules_and_rebalance_events_are_paper_only() -> None:
    split = build_walk_forward_split()
    coverage = audit_dataset_coverage(split)
    assert coverage["live_trading_enabled"] is False
    schedules = default_rebalancing_schedules()
    assert schedules["status"] == "ok"
    assert validate_rebalancing_schedule(schedules["schedules"][1])["status"] == "ok"
    basket = fixture_basket()
    allocation = propose_allocation(basket)["proposal"]
    events = simulate_rebalance_events(allocation, schedules["schedules"][1])
    assert events["events"]
    assert all(event["live_trading_enabled"] is False for event in events["events"])


def test_rolling_simulation_confirm_gate_performance_scorecards_gate_and_evidence(tmp_path) -> None:
    blocked = run_rolling_portfolio_simulation(tmp_path, confirm="")
    assert blocked["status"] == "blocked"
    preview = preview_rolling_portfolio_simulation()
    assert preview["requires_confirm"] == WALK_FORWARD_CONFIRM
    rolling = run_rolling_portfolio_simulation(tmp_path, confirm=WALK_FORWARD_CONFIRM)
    assert rolling["status"] == "completed"
    performance = analyze_walk_forward_performance(rolling)
    assert performance["pass_window_ratio"] >= 0
    scorecards = build_robustness_scorecards(performance, rolling["decay"])
    assert scorecards["scorecards"][0]["grade"] in {"A", "B", "C", "D", "F"}
    gate = evaluate_robustness_governance_gate(scorecards, performance, rolling["split"])
    assert gate["live_trading_enabled"] is False
    evidence = export_walk_forward_evidence(tmp_path, rolling, performance, scorecards, gate)
    assert evidence["manifest"]["split_evidence_present"] is True


def test_decay_and_replacement_default_manual_review_blocks_auto_replace() -> None:
    basket = fixture_basket()
    decay = analyze_allocation_decay(basket)
    assert decay["status"] == "ok"
    replacement = simulate_candidate_replacements(basket, decay)
    assert replacement["status"] == "blocked"
    assert replacement["live_trading_enabled"] is False


def test_dashboard_v2_portfolio_robustness_api_smoke() -> None:
    try:
        from fastapi.testclient import TestClient
    except Exception:
        return
    from binance_spot_bot.dashboard_v2.app import create_dashboard_v2_app

    client = TestClient(create_dashboard_v2_app())
    assert client.get("/api/portfolio-lab/robustness/health").json()["live_trading_enabled"] is False
    assert client.post("/api/portfolio-lab/walk-forward/splits/preview").json()["status"] == "ok"
    assert client.post("/api/portfolio-lab/rolling-simulation/run").json()["status"] == "blocked"

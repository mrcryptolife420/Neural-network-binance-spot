from __future__ import annotations

import json

import pytest

from binance_spot_bot.ab_paper_experiments import run_ab_paper_experiment, write_ab_experiment_report
from binance_spot_bot.experiment_stopping_rules import evaluate_stopping_rules
from binance_spot_bot.governance_evidence_bundle import export_governance_evidence_bundle, verify_governance_evidence_bundle
from binance_spot_bot.governance_simulation import SIMULATION_CASES, run_governance_simulation
from binance_spot_bot.paper_experiment_split import build_split_table
from binance_spot_bot.paper_policy_rollout import create_rollout_plan, validate_rollout_plan, write_rollout_event
from binance_spot_bot.policy_governance import GOVERNANCE_DECISIONS, governance_decision
from binance_spot_bot.policy_lineage import rollback_to_prev_champion
from binance_spot_bot.policy_promotion_gate import evaluate_policy_promotion
from binance_spot_bot.portfolio_policy_registry import PortfolioPolicyMetadata, PortfolioPolicyRegistry, demo_policy
from binance_spot_bot.weekly_governance_report import write_weekly_governance_report


def test_registry_rejects_live_status_and_preserves_lineage_without_secrets(tmp_path):
    registry = PortfolioPolicyRegistry(tmp_path / "registry")
    registry.register(demo_policy("base"))
    registry.register(demo_policy("candidate"))

    with pytest.raises(ValueError):
        registry.register(PortfolioPolicyMetadata(**{**demo_policy("bad").to_dict(), "status": "live"}))
    with pytest.raises(ValueError):
        registry.register(PortfolioPolicyMetadata(**{**demo_policy("bad2").to_dict(), "live_trading_enabled": True}))

    registry.set_champion("base", operator_confirmed=True, evidence_refs=["policy-card"])
    decision = registry.set_champion("candidate", operator_confirmed=True, evidence_refs=["gate-report"])
    payload = json.loads((tmp_path / "registry" / "registry.json").read_text(encoding="utf-8"))

    assert decision.decision == "promoted"
    assert registry.champion().policy_id == "candidate"  # type: ignore[union-attr]
    assert registry.champion().prev_champion_id == "base"  # type: ignore[union-attr]
    assert payload["live_trading_enabled"] is False
    assert len(payload["lineage"]) >= 4
    assert len(payload["decisions"]) >= 2


def test_promotion_gate_requires_full_evidence_and_operator_confirmation(tmp_path):
    card = tmp_path / "policy-card.md"
    manifest = tmp_path / "evidence.json"
    card.write_text("# policy card", encoding="utf-8")
    manifest.write_text(
        json.dumps(
            {
                "benchmark_status": "pass",
                "robustness_score": 0.8,
                "overfit_guard": "pass",
                "paper_approval": "approved",
                "live_trading_enabled": False,
                "signed_endpoint_used": False,
            }
        ),
        encoding="utf-8",
    )
    policy = PortfolioPolicyMetadata(**{**demo_policy("ready").to_dict(), "policy_card_path": str(card), "evidence_manifest_path": str(manifest)})

    blocked = evaluate_policy_promotion(policy, operator_confirmed=False, root=tmp_path)
    allowed = evaluate_policy_promotion(policy, operator_confirmed=True, root=tmp_path)

    assert "operator_confirmation_required" in blocked.reasons
    assert allowed.allowed is True
    assert allowed.live_trading_enabled is False


def test_rollout_split_experiment_stopping_and_decision_acceptance(tmp_path):
    with pytest.raises(ValueError):
        create_rollout_plan("champion", "challenger", ["BTCUSDT"], stage="25pct")
    plan = create_rollout_plan(
        "champion",
        "challenger",
        ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
        stage="25pct",
        challenger_pct=25,
        operator_confirmation="PAPER_POLICY_ROLLOUT",
    )
    assert validate_rollout_plan(plan)["status"] == "ok"
    event_path = write_rollout_event(tmp_path, plan, "created", {"operator": "local"})
    assert event_path.exists()

    split = build_split_table(plan.symbols, plan.alloc_split, seed=42, split_type="time_slice")
    assert split["guardrails"]["paper_only"] is True
    assert len(split["assignments"]) == len(plan.symbols) * 4

    observations = [
        {"symbol": "BTCUSDT", "variant": "champion", "pnl": "1", "drawdown": "1", "fees": "0.1", "trades": 2},
        {"symbol": "ETHUSDT", "variant": "challenger", "pnl": "5", "drawdown": "1", "fees": "0.1", "slippage": "0.1", "trades": 4},
        {"symbol": "BNBUSDT", "variant": "challenger", "pnl": "2", "drawdown": "1", "turnover": "10", "trades": 3},
    ]
    report = run_ab_paper_experiment(plan, observations, seed=42, experiment_type="champion_challenger")
    stop = evaluate_stopping_rules(report, min_samples=2)
    decision = governance_decision(report, stop, operator_confirmed=True, sample_target=2)

    assert report["metrics"]["challenger"]["net_pnl"] > report["metrics"]["champion"]["net_pnl"]
    assert "blocked_rate" in report["metrics"]["challenger"]
    assert stop["status"] == "continue"
    assert decision["decision"] == "promote_challenger"
    assert decision["decision"] in GOVERNANCE_DECISIONS


def test_stopping_rules_and_governance_cover_failure_actions():
    report = run_governance_simulation("policy_violation")
    assert report["stopping"]["status"] == "stop"
    assert report["decision"]["decision"] == "suspend_challenger"

    drawdown = run_governance_simulation("drawdown_breach")
    assert drawdown["stopping"]["status"] == "stop"
    assert drawdown["decision"]["decision"] == "reduce_challenger"

    unconfirmed = run_governance_simulation("operator_not_confirmed")
    assert unconfirmed["decision"]["decision"] == "extend_experiment"
    assert "operator_confirmation_required" in unconfirmed["decision"]["reasons"]


def test_reports_bundle_and_rollback_are_verifiable(tmp_path):
    registry = PortfolioPolicyRegistry(tmp_path / "registry")
    registry.register(demo_policy("old"))
    registry.register(demo_policy("new"))
    registry.set_champion("old", operator_confirmed=True)
    registry.set_champion("new", operator_confirmed=True)
    assert rollback_to_prev_champion(registry, confirm="")["status"] == "blocked"
    assert rollback_to_prev_champion(registry, confirm="PAPER_POLICY_ROLLBACK")["status"] == "rolled_back"

    report = run_governance_simulation("challenger_beats")
    ab_path = write_ab_experiment_report(tmp_path, report["experiment"])
    weekly = write_weekly_governance_report(
        tmp_path,
        {
            "current_champion": "old",
            "experiment": report["experiment"],
            "decision": report["decision"],
            "decisions": [report["decision"]],
            "policies": [{"policy_id": "old", "status": "champion"}, {"policy_id": "new", "status": "challenger"}],
        },
    )
    bundle = export_governance_evidence_bundle(tmp_path, [ab_path, weekly["json"]], {"decision": report["decision"]})
    verification = verify_governance_evidence_bundle(bundle["manifest"])

    for path in weekly.values():
        assert path
    assert bundle["status"] == "ok"
    assert verification["status"] == "ok"
    assert report["live_trading_enabled"] is False


def test_all_governance_simulation_cases_are_deterministic_and_paper_only():
    first = {case: run_governance_simulation(case) for case in SIMULATION_CASES}
    second = {case: run_governance_simulation(case) for case in SIMULATION_CASES}

    assert first.keys() == second.keys()
    for case, payload in first.items():
        assert payload["live_trading_enabled"] is False
        assert payload["decision"]["live_trading_enabled"] is False
        assert payload["decision"]["decision"] == second[case]["decision"]["decision"]

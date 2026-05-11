from __future__ import annotations

import json

from binance_spot_bot.ab_paper_experiments import run_ab_paper_experiment, write_ab_experiment_report
from binance_spot_bot.experiment_stopping_rules import evaluate_stopping_rules
from binance_spot_bot.governance_evidence_bundle import export_governance_evidence_bundle
from binance_spot_bot.governance_simulation import run_governance_simulation
from binance_spot_bot.paper_experiment_split import build_split_table
from binance_spot_bot.paper_policy_rollout import create_rollout_plan
from binance_spot_bot.policy_governance import governance_decision
from binance_spot_bot.policy_lineage import rollback_to_previous_champion
from binance_spot_bot.policy_promotion_gate import evaluate_policy_promotion
from binance_spot_bot.portfolio_policy_registry import PortfolioPolicyMetadata, PortfolioPolicyRegistry, demo_policy
from binance_spot_bot.weekly_governance_report import write_weekly_governance_report


def test_portfolio_policy_registry_promotes_and_preserves_previous_champion(tmp_path):
    registry = PortfolioPolicyRegistry(tmp_path / "portfolio-policies")
    registry.register(demo_policy("champion"))
    registry.register(demo_policy("challenger"))

    first = registry.set_champion("champion", operator_confirmed=True)
    second = registry.set_champion("challenger", operator_confirmed=True)
    champion = registry.champion()

    assert first.decision == "promoted"
    assert second.decision == "promoted"
    assert champion is not None
    assert champion.policy_id == "challenger"
    assert champion.previous_champion_id == "champion"
    assert json.loads((tmp_path / "portfolio-policies" / "registry.json").read_text())["live_trading_enabled"] is False


def test_policy_promotion_gate_blocks_weak_or_unconfirmed_policy():
    weak = PortfolioPolicyMetadata(
        **{**demo_policy("weak").to_dict(), "robustness_score": 0.1, "max_drawdown": "40"}
    )

    result = evaluate_policy_promotion(weak, operator_confirmed=False)

    assert result.allowed is False
    assert "operator_confirmation_required" in result.reasons
    assert "robustness_below_threshold" in result.reasons
    assert result.live_trading_enabled is False


def test_rollout_split_ab_stopping_governance_and_reports(tmp_path):
    plan = create_rollout_plan("champion", "challenger", ["BTCUSDT", "ETHUSDT"], stage="10pct", challenger_pct=50)
    split = build_split_table(plan.symbols, plan.allocation_split, seed=1)
    report = run_ab_paper_experiment(
        plan,
        [
            {"symbol": "BTCUSDT", "variant": "champion", "pnl": "1", "drawdown": "1"},
            {"symbol": "ETHUSDT", "variant": "challenger", "pnl": "3", "drawdown": "1"},
        ],
    )
    stop = evaluate_stopping_rules(report, min_samples=1)
    decision = governance_decision(report, stop, operator_confirmed=True)
    ab_path = write_ab_experiment_report(tmp_path, report)
    weekly = write_weekly_governance_report(tmp_path, {"current_champion": "champion", "decision": decision})
    bundle = export_governance_evidence_bundle(tmp_path, [ab_path], {"decision": decision})

    assert split["live_trading_enabled"] is False
    assert report["status"] == "evaluated"
    assert stop["status"] == "continue"
    assert decision["decision"] in {"promote_challenger", "keep_champion"}
    assert ab_path.exists()
    assert weekly["json"].endswith("weekly_governance_report.json")
    assert bundle["status"] == "ok"


def test_policy_lineage_rollback_requires_confirmation(tmp_path):
    registry = PortfolioPolicyRegistry(tmp_path / "portfolio-policies")
    registry.register(demo_policy("old"))
    registry.register(demo_policy("new"))
    registry.set_champion("old", operator_confirmed=True)
    registry.set_champion("new", operator_confirmed=True)

    blocked = rollback_to_previous_champion(registry, confirm="")
    rolled_back = rollback_to_previous_champion(registry, confirm="PAPER_POLICY_ROLLBACK")

    assert blocked["status"] == "blocked"
    assert rolled_back["status"] == "rolled_back"
    assert registry.champion().policy_id == "old"  # type: ignore[union-attr]


def test_governance_simulation_is_deterministic_and_no_live():
    result = run_governance_simulation("challenger_fails")

    assert result["stopping"]["status"] == "stop"
    assert result["decision"]["decision"] == "suspend_challenger"
    assert result["live_trading_enabled"] is False

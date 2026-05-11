from __future__ import annotations

from .ab_paper_experiments import run_ab_paper_experiment
from .experiment_stopping_rules import evaluate_stopping_rules
from .paper_policy_rollout import create_rollout_plan
from .policy_governance import governance_decision


def run_governance_simulation(case: str = "challenger_beats") -> dict:
    plan = create_rollout_plan("champion", "challenger", ["BTCUSDT", "ETHUSDT"], stage="10pct", challenger_pct=50)
    if case == "challenger_fails":
        observations = [
            {"symbol": "BTCUSDT", "variant": "challenger", "pnl": "-10", "drawdown": "30", "policy_violation": True},
            {"symbol": "ETHUSDT", "variant": "champion", "pnl": "1", "drawdown": "1"},
        ]
    else:
        observations = [
            {"symbol": "BTCUSDT", "variant": "challenger", "pnl": "3", "drawdown": "1"},
            {"symbol": "ETHUSDT", "variant": "champion", "pnl": "1", "drawdown": "1"},
        ]
    experiment = run_ab_paper_experiment(plan, observations)
    stop = evaluate_stopping_rules(experiment, min_samples=1)
    decision = governance_decision(experiment, stop, operator_confirmed=True)
    return {"plan": plan.to_dict(), "experiment": experiment, "stopping": stop, "decision": decision, "live_trading_enabled": False}

from __future__ import annotations

from .ab_paper_experiments import run_ab_paper_experiment
from .experiment_stopping_rules import evaluate_stopping_rules
from .paper_policy_rollout import create_rollout_plan
from .policy_governance import governance_decision

SIMULATION_CASES = {
    "challenger_beats",
    "challenger_fails",
    "too_few_samples",
    "drawdown_breach",
    "data_quality_warning",
    "policy_violation",
    "operator_not_confirmed",
}


def run_governance_simulation(case: str = "challenger_beats") -> dict:
    if case not in SIMULATION_CASES:
        raise ValueError("invalid governance simulation case")
    plan = create_rollout_plan("champion", "challenger", ["BTCUSDT", "ETHUSDT"], stage="10pct", challenger_pct=10)
    observations = _case_observations(case)
    experiment = run_ab_paper_experiment(plan, observations, seed=11)
    stop = evaluate_stopping_rules(experiment, min_samples=1 if case not in {"too_few_samples"} else 10)
    decision = governance_decision(experiment, stop, operator_confirmed=case != "operator_not_confirmed", sample_target=1)
    return {
        "case": case,
        "plan": plan.to_dict(),
        "experiment": experiment,
        "stopping": stop,
        "decision": decision,
        "live_trading_enabled": False,
    }


def _case_observations(case: str) -> list[dict]:
    base = [
        {"symbol": "BTCUSDT", "variant": "champion", "pnl": "1", "drawdown": "1", "trades": 5},
        {"symbol": "ETHUSDT", "variant": "challenger", "pnl": "3", "drawdown": "1", "trades": 5},
    ]
    if case == "challenger_fails":
        return [
            {"symbol": "BTCUSDT", "variant": "champion", "pnl": "3", "drawdown": "1", "trades": 5},
            {"symbol": "ETHUSDT", "variant": "challenger", "pnl": "-5", "drawdown": "8", "trades": 5, "policy_violation": True},
        ]
    if case == "too_few_samples":
        return base[:1]
    if case == "drawdown_breach":
        return [
            {"symbol": "BTCUSDT", "variant": "champion", "pnl": "1", "drawdown": "1", "trades": 5},
            {"symbol": "ETHUSDT", "variant": "challenger", "pnl": "1", "drawdown": "30", "trades": 5},
        ]
    if case == "data_quality_warning":
        return [
            *base,
            {"symbol": "BNBUSDT", "variant": "challenger", "pnl": "1", "drawdown": "1", "data_quality_warning": True},
        ]
    if case == "policy_violation":
        return [
            *base,
            {"symbol": "BNBUSDT", "variant": "challenger", "pnl": "1", "drawdown": "1", "policy_violation": True},
        ]
    return base

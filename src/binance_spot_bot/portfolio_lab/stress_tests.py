from __future__ import annotations

from copy import deepcopy
from typing import Any


SCENARIOS = [
    ("market_drop_shock", -0.08),
    ("high_spread_shock", -0.015),
    ("stale_data_shock", -0.01),
    ("volatility_spike", -0.025),
    ("top_candidate_removed", -0.02),
    ("fees_doubled", -0.002),
]


def run_portfolio_stress_tests(simulation: dict[str, Any]) -> dict[str, Any]:
    base_end = float(simulation.get("ending_quote", simulation.get("starting_quote", 1000.0)))
    start = float(simulation.get("starting_quote", 1000.0))
    results: list[dict[str, Any]] = []
    warnings: list[str] = []
    for scenario_id, shock in SCENARIOS:
        stressed = deepcopy(simulation)
        end = base_end * (1.0 + shock)
        drawdown = max(float(simulation.get("max_drawdown", 0.0)), abs(shock))
        if drawdown > 0.06:
            warnings.append(f"hard scenario warning: {scenario_id}")
        results.append(
            {
                "scenario_id": scenario_id,
                "starting_quote": start,
                "stressed_ending_quote": round(end, 6),
                "stressed_paper_pnl": round(end - start, 6),
                "stressed_max_drawdown": round(drawdown, 6),
                "source_simulation_id": stressed.get("simulation_id"),
            }
        )
    return {"status": "warn" if warnings else "ok", "results": results, "warnings": warnings, "live_trading_enabled": False}


from __future__ import annotations

import hashlib
import json
import statistics
import time
from dataclasses import asdict, dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from .config import BotSettings
from .paper_portfolio_ops import PaperPortfolioPlan
from .redaction import redact_payload


@dataclass(frozen=True)
class StressScenario:
    name: str
    price_shock_bps: int = 0
    spread_shock_bps: int = 0
    liquidity_haircut: Decimal = Decimal("0")
    correlation_shock: Decimal = Decimal("0")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DEFAULT_SCENARIOS = [
    StressScenario("bull_momentum", price_shock_bps=150, spread_shock_bps=5),
    StressScenario("bear_liquidity", price_shock_bps=-300, spread_shock_bps=80, liquidity_haircut=Decimal("0.35")),
    StressScenario("range_chop", price_shock_bps=-50, spread_shock_bps=20),
    StressScenario("correlation_break", price_shock_bps=-150, spread_shock_bps=40, correlation_shock=Decimal("0.50")),
]


def replay_portfolio_scenario(plan: PaperPortfolioPlan, scenario: StressScenario) -> dict[str, Any]:
    rows = []
    total_loss = Decimal("0")
    total_budget = Decimal("0")
    for allocation in plan.allocations:
        budget = Decimal(str(allocation["quote_budget"]))
        total_budget += budget
        price_loss = budget * Decimal(abs(min(scenario.price_shock_bps, 0))) / Decimal("10000")
        spread_cost = budget * Decimal(scenario.spread_shock_bps) / Decimal("10000")
        liquidity_cost = budget * scenario.liquidity_haircut
        loss = (price_loss + spread_cost + liquidity_cost).quantize(Decimal("0.01"))
        total_loss += loss
        rows.append(
            {
                "strategy_id": allocation["strategy_id"],
                "symbol": allocation["symbol"],
                "quote_budget": str(budget),
                "stressed_loss": str(loss),
                "scenario": scenario.name,
            }
        )
    drawdown_pct = float((total_loss / total_budget) if total_budget else Decimal("0"))
    return {
        "scenario": scenario.to_dict(),
        "rows": rows,
        "total_stressed_loss": str(total_loss),
        "drawdown_pct": round(drawdown_pct, 6),
        "status": "pass" if drawdown_pct <= 0.08 else "review",
    }


def benchmark_allocations(plan: PaperPortfolioPlan, scenarios: list[StressScenario] | None = None) -> dict[str, Any]:
    scenarios = scenarios or DEFAULT_SCENARIOS
    replays = [replay_portfolio_scenario(plan, scenario) for scenario in scenarios]
    drawdowns = [float(row["drawdown_pct"]) for row in replays]
    robustness = max(0.0, 1.0 - (statistics.mean(drawdowns) if drawdowns else 0.0))
    return {
        "status": "pass" if all(row["status"] == "pass" for row in replays) else "review",
        "robustness_score": round(robustness, 6),
        "replays": replays,
        "reproducibility_hash": _hash_payload({"plan": plan.to_dict(), "scenarios": [item.to_dict() for item in scenarios]}),
        "live_trading_enabled": False,
    }


def validate_rotation_robustness(rotation_rows: list[dict[str, Any]], max_pause_rate: float = 0.50) -> dict[str, Any]:
    if not rotation_rows:
        return {"status": "blocked", "reason": "no_rotation_rows"}
    pauses = sum(1 for row in rotation_rows if row.get("action") == "pause")
    pause_rate = pauses / len(rotation_rows)
    return {"status": "pass" if pause_rate <= max_pause_rate else "review", "pause_rate": round(pause_rate, 4), "max_pause_rate": max_pause_rate}


def correlation_stress(symbol_returns: dict[str, list[float]]) -> dict[str, Any]:
    symbols = sorted(symbol_returns)
    pairs = []
    for left_index, left in enumerate(symbols):
        for right in symbols[left_index + 1 :]:
            corr = _correlation(symbol_returns[left], symbol_returns[right])
            pairs.append({"pair": f"{left}/{right}", "correlation": round(corr, 6), "status": "crowded" if corr > 0.80 else "ok"})
    return {"status": "review" if any(row["status"] == "crowded" for row in pairs) else "pass", "pairs": pairs}


def write_benchmark_report(settings: BotSettings, benchmark: dict[str, Any]) -> dict[str, str]:
    out = settings.data_dir / "paper-portfolio" / "benchmarks"
    out.mkdir(parents=True, exist_ok=True)
    stamp = int(time.time() * 1000)
    json_path = out / f"portfolio-benchmark-{stamp}.json"
    latest_path = out / "latest.json"
    md_path = out / "portfolio-benchmark-report.md"
    payload = redact_payload(benchmark)
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    latest_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Paper Portfolio Benchmark Report",
                "",
                f"Status: {benchmark.get('status')}",
                f"Robustness: {benchmark.get('robustness_score')}",
                f"Replay hash: {benchmark.get('reproducibility_hash')}",
                "Live trading: disabled",
            ]
        ),
        encoding="utf-8",
    )
    return {"json": str(json_path), "latest": str(latest_path), "markdown": str(md_path)}


def _correlation(left: list[float], right: list[float]) -> float:
    count = min(len(left), len(right))
    if count < 2:
        return 0.0
    left = left[-count:]
    right = right[-count:]
    left_mean = statistics.mean(left)
    right_mean = statistics.mean(right)
    numerator = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right))
    left_den = sum((a - left_mean) ** 2 for a in left) ** 0.5
    right_den = sum((b - right_mean) ** 2 for b in right) ** 0.5
    return numerator / (left_den * right_den) if left_den and right_den else 0.0


def _hash_payload(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, default=str, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

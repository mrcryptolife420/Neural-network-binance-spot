from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, redact_value, status_from_blockers

NO_LIVE_STATEMENT = "DEMO-TO-LIVE TRAINING - NO LIVE TRADING"
PUBLIC_OR_DEMO_ONLY = "PUBLIC OR DEMO/TESTNET DATA ONLY"
NOT_ADVICE = "TRAINING OUTPUT IS RESEARCH EVIDENCE, NOT FINANCIAL ADVICE"


@dataclass(frozen=True)
class DemoSessionTarget:
    minimum_demo_sessions: int = 3
    minimum_total_runtime_minutes: int = 120
    minimum_candles: int = 500
    minimum_signals: int = 30
    minimum_allow_risk_decisions: int = 10
    minimum_block_risk_decisions: int = 5
    minimum_order_previews: int = 10
    minimum_test_orders: int = 3
    minimum_demo_orders: int = 3
    minimum_fills: int = 10
    minimum_rejections_or_cancellations: int = 2
    minimum_spread_samples: int = 100
    minimum_latency_samples: int = 10
    minimum_reconciliation_runs: int = 3
    required_market_regimes: list[str] = field(default_factory=lambda: ["calm", "volatile", "low_volume", "high_spread", "trending", "ranging"])


def default_demo_session_target() -> DemoSessionTarget:
    return DemoSessionTarget()


def calculate_demo_session_target_progress(target: DemoSessionTarget, session_summaries: list[dict[str, Any]]) -> dict[str, Any]:
    totals = {
        "demo_sessions": len(session_summaries),
        "total_runtime_minutes": sum(int(item.get("runtime_minutes", 0)) for item in session_summaries),
        "candles": sum(int(item.get("candles", 0)) for item in session_summaries),
        "signals": sum(int(item.get("signals", 0)) for item in session_summaries),
        "allow_risk_decisions": sum(int(item.get("allow_risk_decisions", 0)) for item in session_summaries),
        "block_risk_decisions": sum(int(item.get("block_risk_decisions", 0)) for item in session_summaries),
        "order_previews": sum(int(item.get("order_previews", 0)) for item in session_summaries),
        "test_orders": sum(int(item.get("test_orders", 0)) for item in session_summaries),
        "demo_orders": sum(int(item.get("demo_orders", 0)) for item in session_summaries),
        "fills": sum(int(item.get("fills", 0)) for item in session_summaries),
        "rejections_or_cancellations": sum(int(item.get("rejections_or_cancellations", 0)) for item in session_summaries),
        "spread_samples": sum(int(item.get("spread_samples", 0)) for item in session_summaries),
        "latency_samples": sum(int(item.get("latency_samples", 0)) for item in session_summaries),
        "reconciliation_runs": sum(int(item.get("reconciliation_runs", 0)) for item in session_summaries),
    }
    regimes = sorted({regime for item in session_summaries for regime in item.get("market_regimes", [])})
    required = {
        "demo_sessions": target.minimum_demo_sessions,
        "total_runtime_minutes": target.minimum_total_runtime_minutes,
        "candles": target.minimum_candles,
        "signals": target.minimum_signals,
        "allow_risk_decisions": target.minimum_allow_risk_decisions,
        "block_risk_decisions": target.minimum_block_risk_decisions,
        "order_previews": target.minimum_order_previews,
        "test_orders": target.minimum_test_orders,
        "demo_orders": target.minimum_demo_orders,
        "fills": target.minimum_fills,
        "rejections_or_cancellations": target.minimum_rejections_or_cancellations,
        "spread_samples": target.minimum_spread_samples,
        "latency_samples": target.minimum_latency_samples,
        "reconciliation_runs": target.minimum_reconciliation_runs,
    }
    missing = [key for key, needed in required.items() if totals[key] < needed]
    missing_regimes = [item for item in target.required_market_regimes if item not in regimes]
    blockers = []
    warnings = []
    if any(str(item.get("mode", "")).lower() == "live" or item.get("live_trading_enabled") for item in session_summaries):
        blockers.append("live event contamination")
    for item in session_summaries:
        if "runtime_minutes" not in item:
            warnings.append("session missing runtime_minutes")
    score_parts = [min(1.0, totals[key] / max(1, needed)) for key, needed in required.items()]
    score_parts.append(1.0 - len(missing_regimes) / max(1, len(target.required_market_regimes)))
    progress_percent = round(sum(score_parts) / len(score_parts) * 100.0, 4)
    if missing or missing_regimes:
        blockers.append("demo collection targets incomplete")
    return redact_value(
        {
            "status": status_from_blockers(blockers, warnings),
            "target": asdict(target),
            "totals": totals,
            "market_regimes": regimes,
            "missing_targets": missing,
            "missing_market_regimes": missing_regimes,
            "progress_percent": progress_percent,
            "blockers": blockers,
            "warnings": warnings,
            "next_recommended_collection_steps": missing[:5] + missing_regimes[:3],
            "no_live_statement": NO_LIVE_STATEMENT,
            "public_or_demo_data_only_statement": PUBLIC_OR_DEMO_ONLY,
            "not_financial_advice_statement": NOT_ADVICE,
            "live_execution_enabled": False,
            "live_trading_enabled": False,
        }
    )


def fixture_complete_sessions() -> list[dict[str, Any]]:
    regime_groups = [
        ["calm", "volatile"],
        ["low_volume", "high_spread"],
        ["trending", "ranging"],
    ]
    return [
        {
            "session_id": f"demo-{idx}",
            "runtime_minutes": 45,
            "candles": 200,
            "signals": 12,
            "allow_risk_decisions": 5,
            "block_risk_decisions": 3,
            "order_previews": 4,
            "test_orders": 2,
            "demo_orders": 2,
            "fills": 4,
            "rejections_or_cancellations": 1,
            "spread_samples": 50,
            "latency_samples": 4,
            "reconciliation_runs": 1,
            "market_regimes": regime_groups[idx],
            "live_trading_enabled": False,
        }
        for idx in range(3)
    ]


def write_demo_session_target_report(root: Path, report: dict[str, Any]) -> dict[str, Any]:
    return json_write(root / "data" / "live-training" / "demo-targets" / "demo_session_target_report.json", report)

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Any

from binance_spot_bot.redaction import redact_payload
from binance_spot_bot.market_intelligence.market_snapshot_cache import demo_market_snapshot
from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT, PAPER_ONLY_CONFIRM


@dataclass(frozen=True)
class PaperExperimentJobResult:
    job_id: str
    symbol: str
    interval: str
    strategy_id: str
    model_alias: str
    risk_preset: str
    status: str
    candle_count: int
    signal_count: int
    fill_count: int
    block_count: int
    paper_pnl: str
    max_drawdown: str
    fees: str
    exposure_summary: dict[str, Any]
    data_quality_warnings: tuple[str, ...] = ()
    runtime_messages: tuple[str, ...] = ()
    report_paths: tuple[str, ...] = ()
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class PaperExperimentRunnerReport:
    run_id: str
    queue_id: str
    status: str
    results: tuple[PaperExperimentJobResult, ...]
    started_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    no_live_statement: str = NO_LIVE_STATEMENT
    no_advice_statement: str = NO_ADVICE_STATEMENT
    live_trading_enabled: bool = False


def _simulate_job(job: dict[str, Any]) -> PaperExperimentJobResult:
    snapshot = demo_market_snapshot(str(job.get("symbol", "BTCUSDT")))
    klines = snapshot["klines"]
    start = Decimal(str(klines[0][4]))
    end = Decimal(str(klines[-1][4]))
    pnl = ((end - start) * Decimal("0.01")).quantize(Decimal("0.0001"))
    drawdown = min(Decimal("0"), pnl / Decimal("2")).quantize(Decimal("0.0001"))
    return PaperExperimentJobResult(
        job_id=str(job.get("job_id")),
        symbol=str(job.get("symbol")),
        interval=str(job.get("interval", "1m")),
        strategy_id=str(job.get("strategy_id", "momentum_research")),
        model_alias=str(job.get("model_alias", "rule_based")),
        risk_preset=str(job.get("risk_preset", "conservative")),
        status="completed",
        candle_count=len(klines),
        signal_count=max(1, len(klines) // 10),
        fill_count=2,
        block_count=0,
        paper_pnl=str(pnl),
        max_drawdown=str(drawdown),
        fees="0.02",
        exposure_summary={"max_quote": str(job.get("starting_quote", "1000")), "paper_only": True},
        runtime_messages=("fixture paper simulation",),
    )


def run_paper_experiment_queue(queue_payload: dict[str, Any], *, confirm: str = "", resume: bool = False) -> dict[str, Any]:
    if confirm != PAPER_ONLY_CONFIRM:
        return {"status": "blocked", "blockers": [f"queue run requires confirm {PAPER_ONLY_CONFIRM}"], "live_trading_enabled": False}
    if queue_payload.get("live_trading_enabled"):
        return {"status": "blocked", "blockers": ["live queue blocked"], "live_trading_enabled": False}
    results = tuple(_simulate_job(job) for job in queue_payload.get("jobs", []) if job.get("status", "queued") in {"queued", "failed"} or resume)
    report = PaperExperimentRunnerReport(str(int(time.time() * 1000)), str(queue_payload.get("queue_id", "fixture")), "ok", results)
    return redact_payload(asdict(report))

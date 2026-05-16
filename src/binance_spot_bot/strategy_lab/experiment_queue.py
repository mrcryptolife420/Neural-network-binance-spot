from __future__ import annotations

import hashlib
import time
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Any

from binance_spot_bot.redaction import redact_payload
from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT

ALLOWED_STRATEGIES = {"momentum_research", "mean_reversion_research", "baseline_hold_research"}
ALLOWED_MODELS = {"rule_based", "demo-model", "candidate", "paper_candidate"}
ALLOWED_RISK = {"conservative", "balanced", "research_aggressive"}
ALLOWED_SOURCES = {"cached_klines", "fixture", "demo_replay", "public_rest_cache"}


def _hash_payload(payload: dict[str, Any]) -> str:
    return hashlib.sha256(str(redact_payload(payload)).encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class StrategyExperimentJob:
    job_id: str
    candidate_id: str
    symbol: str
    interval: str = "1m"
    data_source: str = "fixture"
    strategy_id: str = "momentum_research"
    model_alias: str = "rule_based"
    risk_preset: str = "conservative"
    seed: int = 1
    window: int = 30
    max_steps: int = 30
    starting_quote: str = "1000"
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    status: str = "queued"
    blockers: tuple[str, ...] = ()
    expected_artifacts: tuple[str, ...] = ("job_result_json", "job_result_markdown")
    no_live_statement: str = NO_LIVE_STATEMENT
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class StrategyExperimentQueue:
    queue_id: str
    name: str
    jobs: tuple[StrategyExperimentJob, ...]
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    status: str = "queued"
    no_live_statement: str = NO_LIVE_STATEMENT
    no_advice_statement: str = NO_ADVICE_STATEMENT
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class StrategyExperimentQueueValidation:
    status: str
    blockers: tuple[str, ...]
    warnings: tuple[str, ...] = ()
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class StrategyExperimentQueueManifest:
    queue_id: str
    job_count: int
    payload_hash: str
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False


def queue_to_dict(queue: StrategyExperimentQueue) -> dict[str, Any]:
    return redact_payload(asdict(queue))


def validate_queue(queue: StrategyExperimentQueue, *, max_jobs: int = 50) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    if len(queue.jobs) > max_jobs:
        blockers.append("queue exceeds max jobs")
    for job in queue.jobs:
        if job.job_id in seen:
            blockers.append(f"duplicate job: {job.job_id}")
        seen.add(job.job_id)
        if job.strategy_id not in ALLOWED_STRATEGIES:
            blockers.append(f"unsupported strategy: {job.strategy_id}")
        if job.model_alias not in ALLOWED_MODELS:
            blockers.append(f"unsupported model alias: {job.model_alias}")
        if job.risk_preset not in ALLOWED_RISK:
            blockers.append(f"unsupported risk preset: {job.risk_preset}")
        if job.data_source not in ALLOWED_SOURCES:
            blockers.append(f"unsupported data source: {job.data_source}")
        if job.live_trading_enabled:
            blockers.append(f"live job blocked: {job.job_id}")
        if Decimal(str(job.starting_quote)) <= 0:
            blockers.append(f"starting quote must be positive: {job.job_id}")
        if job.max_steps < 5:
            warnings.append(f"short experiment window: {job.job_id}")
    return redact_payload(asdict(StrategyExperimentQueueValidation("ok" if not blockers else "blocked", tuple(blockers), tuple(warnings))))


def queue_manifest(queue: StrategyExperimentQueue) -> dict[str, Any]:
    payload = queue_to_dict(queue)
    return redact_payload(asdict(StrategyExperimentQueueManifest(queue.queue_id, len(queue.jobs), _hash_payload(payload))))


def build_queue_from_candidates(candidates: list[dict[str, Any]], *, preset: str = "small_safe_smoke", name: str = "Strategy Lab Queue") -> dict[str, Any]:
    jobs: list[StrategyExperimentJob] = []
    for idx, candidate in enumerate(candidates):
        symbol = str(candidate.get("symbol", "BTCUSDT")).upper()
        candidate_id = str(candidate.get("candidate_id", symbol))
        job_id = hashlib.sha256(f"{preset}|{candidate_id}|{symbol}|{idx}".encode("utf-8")).hexdigest()[:16]
        jobs.append(
            StrategyExperimentJob(
                job_id=job_id,
                candidate_id=candidate_id,
                symbol=symbol,
                interval=str(candidate.get("interval", "1m")),
                data_source=str(candidate.get("data_source", "fixture")),
                strategy_id=str(candidate.get("strategy_id", "momentum_research")),
                model_alias=str(candidate.get("model_alias", "rule_based")),
                risk_preset=str(candidate.get("risk_preset", "conservative")),
            )
        )
    queue_id = hashlib.sha256(f"{preset}|{','.join(job.symbol for job in jobs)}".encode("utf-8")).hexdigest()[:16]
    queue = StrategyExperimentQueue(queue_id, name, tuple(jobs))
    payload = queue_to_dict(queue)
    payload["validation"] = validate_queue(queue)
    payload["manifest"] = queue_manifest(queue)
    return payload

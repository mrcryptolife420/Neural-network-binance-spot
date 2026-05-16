from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .common import status_from_blockers, to_plain


@dataclass(frozen=True)
class RebalancingSchedule:
    schedule_id: str
    schedule_type: str
    interval_steps: int = 12
    allocation_drift_threshold_pct: float = 7.5
    drawdown_threshold_pct: float = 8.0
    volatility_threshold: float = 0.03
    candidate_decay_threshold: float = 0.25
    max_rebalances: int = 6
    min_steps_between_rebalances: int = 6
    paper_only: bool = True
    live_trading_enabled: bool = False


def default_rebalancing_schedules() -> dict[str, Any]:
    schedules = [
        RebalancingSchedule("no-rebalance", "no_rebalance", interval_steps=9999, max_rebalances=0),
        RebalancingSchedule("fixed-interval", "fixed_interval", interval_steps=12),
        RebalancingSchedule("drawdown-guarded", "drawdown_guarded", interval_steps=12, drawdown_threshold_pct=6.0),
        RebalancingSchedule("candidate-decay-guarded", "candidate_decay_guarded", interval_steps=12, candidate_decay_threshold=0.2),
    ]
    return {"status": "ok", "schedules": [to_plain(item) for item in schedules], "live_trading_enabled": False}


def validate_rebalancing_schedule(schedule: dict[str, Any] | RebalancingSchedule) -> dict[str, Any]:
    payload = to_plain(schedule)
    blockers = []
    if payload.get("live_trading_enabled"):
        blockers.append("schedule live_trading_enabled must be false")
    if not payload.get("paper_only", True):
        blockers.append("schedule must be paper_only")
    if int(payload.get("interval_steps", 0)) <= 0:
        blockers.append("interval_steps must be positive")
    if int(payload.get("max_rebalances", 0)) < 0:
        blockers.append("max_rebalances must be non-negative")
    if float(payload.get("allocation_drift_threshold_pct", 0)) < 0:
        blockers.append("allocation drift threshold must be non-negative")
    return {"status": status_from_blockers(blockers), "blockers": blockers, "schedule": payload, "live_trading_enabled": False}


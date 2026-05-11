from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload

ROLLOUT_STAGES = {
    "observe_only": 0,
    "canary": 5,
    "10pct": 10,
    "25pct": 25,
    "50pct": 50,
    "full_paper": 100,
}
STAGE_CONFIRMATION = "PAPER_POLICY_ROLLOUT"


@dataclass(frozen=True)
class RolloutPlan:
    rollout_id: str
    champion_policy_id: str
    challenger_policy_id: str
    rollout_stage: str
    alloc_split: dict[str, str]
    symbols: list[str]
    max_duration_minutes: int = 60
    min_sample_count: int = 30
    stopping_rules: list[str] = field(
        default_factory=lambda: [
            "max_drawdown",
            "underperform_champion",
            "data_quality",
            "policy_violation",
            "excess_turnover",
        ]
    )
    success_rules: list[str] = field(default_factory=lambda: ["better_score", "drawdown_ok", "samples_ok", "no_policy_violations"])
    rollback_target: str = "prev_champion"
    operator_confirmation: str = ""
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    @property
    def allocation_split(self) -> dict[str, str]:
        return self.alloc_split

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def create_rollout_plan(
    champion_policy_id: str,
    challenger_policy_id: str,
    symbols: list[str],
    stage: str = "observe_only",
    challenger_pct: int | None = None,
    operator_confirmation: str = "",
    max_duration_minutes: int = 60,
    min_sample_count: int = 30,
) -> RolloutPlan:
    if stage not in ROLLOUT_STAGES:
        raise ValueError("invalid rollout stage")
    stage_pct = ROLLOUT_STAGES[stage]
    if challenger_pct is None:
        challenger_pct = stage_pct
    challenger_pct = int(challenger_pct)
    if challenger_pct < 0 or challenger_pct > 100:
        raise ValueError("challenger allocation must be between 0 and 100")
    if stage in {"25pct", "50pct", "full_paper"} and operator_confirmation != STAGE_CONFIRMATION:
        raise ValueError("stage increase requires PAPER_POLICY_ROLLOUT confirmation")
    if not symbols:
        raise ValueError("symbols are required")
    normalized_symbols = sorted({symbol.strip().upper() for symbol in symbols if symbol.strip()})
    if not normalized_symbols:
        raise ValueError("symbols are required")
    return RolloutPlan(
        rollout_id=f"rollout-{int(time.time() * 1000)}",
        champion_policy_id=champion_policy_id,
        challenger_policy_id=challenger_policy_id,
        rollout_stage=stage,
        alloc_split={"champion": str(100 - challenger_pct), "challenger": str(challenger_pct)},
        symbols=normalized_symbols,
        max_duration_minutes=max_duration_minutes,
        min_sample_count=min_sample_count,
        operator_confirmation=operator_confirmation,
        live_trading_enabled=False,
    )


def validate_rollout_plan(plan: RolloutPlan) -> dict[str, Any]:
    reasons: list[str] = []
    challenger_pct = int(float(plan.alloc_split.get("challenger", "0")))
    champion_pct = int(float(plan.alloc_split.get("champion", "0")))
    if champion_pct + challenger_pct != 100:
        reasons.append("allocation_split_must_equal_100")
    if challenger_pct > ROLLOUT_STAGES.get(plan.rollout_stage, -1):
        reasons.append("challenger_allocation_exceeds_stage_budget")
    if plan.live_trading_enabled:
        reasons.append("live_trading_not_allowed")
    if plan.max_duration_minutes <= 0:
        reasons.append("duration_must_be_positive")
    if plan.min_sample_count <= 0:
        reasons.append("min_sample_count_must_be_positive")
    return {"status": "ok" if not reasons else "blocked", "reasons": reasons, "live_trading_enabled": False}


def write_rollout_event(root: Path, plan: RolloutPlan, event: str, payload: dict[str, Any] | None = None) -> Path:
    out = root / "policy-governance" / "rollouts" / plan.rollout_id
    out.mkdir(parents=True, exist_ok=True)
    record = redact_payload(
        {
            "rollout_id": plan.rollout_id,
            "event": event,
            "plan": plan.to_dict(),
            "payload": payload or {},
            "created_at_ms": int(time.time() * 1000),
            "live_trading_enabled": False,
        }
    )
    path = out / f"{int(time.time() * 1000)}-{event}.json"
    path.write_text(json.dumps(record, indent=2, default=str), encoding="utf-8")
    return path

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class RolloutPlan:
    rollout_id: str
    champion_policy_id: str
    challenger_policy_id: str
    rollout_stage: str
    allocation_split: dict[str, str]
    symbols: list[str]
    max_duration_minutes: int = 60
    min_sample_count: int = 30
    stopping_rules: list[str] = field(default_factory=lambda: ["max_drawdown", "underperform_champion", "data_quality"])
    success_rules: list[str] = field(default_factory=lambda: ["better_score", "drawdown_ok", "samples_ok"])
    rollback_target: str = "previous_champion"
    operator_confirmation: str = ""
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def create_rollout_plan(
    champion_policy_id: str,
    challenger_policy_id: str,
    symbols: list[str],
    *,
    stage: str = "observe_only",
    challenger_pct: int = 10,
    operator_confirmation: str = "",
) -> RolloutPlan:
    if stage not in {"observe_only", "canary", "10pct", "25pct", "50pct", "full_paper"}:
        raise ValueError("invalid rollout stage")
    if stage in {"25pct", "50pct", "full_paper"} and operator_confirmation != "PAPER_POLICY_ROLLOUT":
        raise ValueError("stage increase requires PAPER_POLICY_ROLLOUT confirmation")
    challenger_pct = max(0, min(100, challenger_pct))
    return RolloutPlan(
        rollout_id=f"rollout-{int(time.time() * 1000)}",
        champion_policy_id=champion_policy_id,
        challenger_policy_id=challenger_policy_id,
        rollout_stage=stage,
        allocation_split={"champion": str(100 - challenger_pct), "challenger": str(challenger_pct)},
        symbols=[symbol.upper() for symbol in symbols],
        operator_confirmation=operator_confirmation,
    )

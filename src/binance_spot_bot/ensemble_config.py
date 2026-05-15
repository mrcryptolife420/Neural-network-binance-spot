from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

FORBIDDEN_ENSEMBLE_ALIASES = {"champion_live", "live_approved", "auto_live", "live_portfolio", "live_allocation"}


@dataclass(frozen=True)
class EnsembleMember:
    alias: str
    weight: float
    strategy: str = "default"
    symbol: str = "BTCUSDT"
    health_score: int = 100
    drift_status: str = "ok"


@dataclass(frozen=True)
class EnsembleVotingPolicy:
    min_confidence: float = 0.2
    tie_breaker: str = "HOLD"


@dataclass(frozen=True)
class EnsembleWeightPolicy:
    max_member_weight: float = 0.6
    max_total_weight: float = 1.0
    block_health_below: int = 50


@dataclass(frozen=True)
class EnsembleConfig:
    ensemble_id: str
    members: list[EnsembleMember]
    voting: EnsembleVotingPolicy = field(default_factory=EnsembleVotingPolicy)
    weights: EnsembleWeightPolicy = field(default_factory=EnsembleWeightPolicy)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_ensemble_config(config: EnsembleConfig) -> dict[str, Any]:
    blockers: list[str] = []
    aliases = {member.alias for member in config.members}
    if aliases & FORBIDDEN_ENSEMBLE_ALIASES:
        blockers.append("forbidden_live_alias")
    if sum(member.weight for member in config.members) > config.weights.max_total_weight:
        blockers.append("weight_budget_exceeded")
    if any(member.weight > config.weights.max_member_weight for member in config.members):
        blockers.append("member_weight_exceeded")
    if any(member.health_score < config.weights.block_health_below for member in config.members):
        blockers.append("member_health_blocks_allocation")
    if any(member.drift_status in {"blocked", "critical"} for member in config.members):
        blockers.append("critical_drift_blocks_allocation")
    return {"status": "ok" if not blockers else "blocked", "blockers": blockers, "config": config.to_dict(), "live_trading_enabled": False}


def ensemble_config(models: list[str]) -> dict[str, Any]:
    config = EnsembleConfig("legacy", [EnsembleMember(alias=model, weight=1 / max(1, len(models))) for model in models])
    return validate_ensemble_config(config) | {"models": models}

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

FORBIDDEN_DOWNGRADE_ALIASES = {"champion_live", "live_approved", "auto_live"}
ALLOWED_DOWNGRADE_ALIASES = {"candidate", "paper_candidate", "shadow_candidate", "demo_candidate", "champion_paper", "champion_shadow"}


@dataclass(frozen=True)
class DriftThresholds:
    feature_drift_warn: float = 0.2
    prediction_drift_warn: float = 0.2
    confidence_drift_warn: float = 0.2


@dataclass(frozen=True)
class PerformanceThresholds:
    min_pnl_quote: float = -10.0
    max_drawdown_quote: float = 25.0
    min_win_rate: float = 0.35


@dataclass(frozen=True)
class DowngradePolicy:
    enabled: bool = True
    allowed_aliases: set[str] = field(default_factory=lambda: set(ALLOWED_DOWNGRADE_ALIASES))
    forbidden_aliases: set[str] = field(default_factory=lambda: set(FORBIDDEN_DOWNGRADE_ALIASES))
    confirmation_phrase: str = "DOWNGRADE_PAPER_MODEL"


@dataclass(frozen=True)
class MonitoringSchedulePolicy:
    interval_minutes: int = 15
    local_only: bool = True


@dataclass(frozen=True)
class ModelMonitoringScope:
    monitored_aliases: list[str] = field(default_factory=lambda: ["candidate", "champion_paper"])
    baseline_model_alias: str = "baseline"
    champion_alias: str = "champion_paper"
    candidate_aliases: list[str] = field(default_factory=lambda: ["candidate", "paper_candidate", "shadow_candidate"])


@dataclass(frozen=True)
class ModelMonitoringConfig:
    scope: ModelMonitoringScope = field(default_factory=ModelMonitoringScope)
    feature_dataset_id: str = "unknown"
    feature_schema_hash: str = "unknown"
    training_baseline_window: int = 250
    runtime_monitoring_window: int = 100
    min_observations: int = 5
    drift: DriftThresholds = field(default_factory=DriftThresholds)
    performance: PerformanceThresholds = field(default_factory=PerformanceThresholds)
    downgrade: DowngradePolicy = field(default_factory=DowngradePolicy)
    schedule: MonitoringSchedulePolicy = field(default_factory=MonitoringSchedulePolicy)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["downgrade"]["allowed_aliases"] = sorted(self.downgrade.allowed_aliases)
        payload["downgrade"]["forbidden_aliases"] = sorted(self.downgrade.forbidden_aliases)
        return payload


def validate_model_monitoring_config(config: ModelMonitoringConfig) -> dict[str, Any]:
    blockers: list[str] = []
    aliases = set(config.scope.monitored_aliases + config.scope.candidate_aliases + [config.scope.champion_alias])
    if aliases & config.downgrade.forbidden_aliases:
        blockers.append("forbidden_live_alias_in_scope")
    if config.live_trading_enabled or not config.schedule.local_only:
        blockers.append("monitoring_must_be_local_no_live")
    if config.min_observations <= 0:
        blockers.append("min_observations_required")
    return {"status": "ok" if not blockers else "blocked", "blockers": blockers, "config": config.to_dict(), "live_trading_enabled": False}


def model_monitoring_config() -> dict[str, Any]:
    config = ModelMonitoringConfig()
    return validate_model_monitoring_config(config)

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class TrainingDataBinding:
    feature_dataset_id: str
    label_dataset_id: str
    feature_schema_hash: str
    label_schema_hash: str = "labels-v1"
    dataset_manifest_path: str = ""


@dataclass(frozen=True)
class TrainingModelSpec:
    model_type: str = "tiny_neural_signal"
    hidden_size: int = 6
    epochs: int = 20
    learning_rate: float = 0.03
    random_seed: int = 7


@dataclass(frozen=True)
class TrainingSplitPolicy:
    train_ratio: float = 0.6
    validation_ratio: float = 0.2
    walk_forward_required: bool = True


@dataclass(frozen=True)
class TrainingCostAssumptions:
    fee_bps: float = 10.0
    slippage_bps: float = 5.0
    spread_bps: float = 0.0


@dataclass(frozen=True)
class TrainingRiskAssumptions:
    min_trade_count: int = 1
    max_drawdown_quote: float = 1000.0
    candidate_beats_baseline_required: bool = True


@dataclass(frozen=True)
class TrainingValidationPolicy:
    no_live_required: bool = True
    leakage_pass_required: bool = True
    operator_confirmation_required: bool = True


@dataclass(frozen=True)
class TrainingJobConfig:
    job_id: str
    experiment_name: str
    data: TrainingDataBinding
    model: TrainingModelSpec = field(default_factory=TrainingModelSpec)
    split: TrainingSplitPolicy = field(default_factory=TrainingSplitPolicy)
    costs: TrainingCostAssumptions = field(default_factory=TrainingCostAssumptions)
    risk: TrainingRiskAssumptions = field(default_factory=TrainingRiskAssumptions)
    validation: TrainingValidationPolicy = field(default_factory=TrainingValidationPolicy)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


def validate_training_config(config: TrainingJobConfig, *, expected_feature_schema_hash: str | None = None) -> dict[str, Any]:
    blockers: list[str] = []
    if config.live_trading_enabled or not config.validation.no_live_required:
        blockers.append("live_trading_not_allowed")
    if not config.data.feature_dataset_id:
        blockers.append("feature_dataset_missing")
    if not config.data.label_dataset_id:
        blockers.append("label_dataset_missing")
    if config.data.dataset_manifest_path and not Path(config.data.dataset_manifest_path).exists():
        blockers.append("dataset_manifest_missing")
    if expected_feature_schema_hash and config.data.feature_schema_hash != expected_feature_schema_hash:
        blockers.append("feature_schema_mismatch")
    if config.model.model_type not in {"rule_baseline", "tiny_neural_signal", "future_optional_adapter"}:
        blockers.append("unsupported_model_type")
    if config.model.epochs <= 0 or config.model.learning_rate <= 0:
        blockers.append("invalid_training_hyperparameters")
    return {
        "status": "ok" if not blockers else "blocked",
        "blockers": blockers,
        "config": config.to_dict(),
        "live_trading_enabled": False,
    }

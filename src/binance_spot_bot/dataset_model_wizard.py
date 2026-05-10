from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from .dataset_governance import DatasetManifest, build_dataset_manifest
from .types import Candle, FeatureRow, LabelRow


@dataclass(frozen=True)
class DatasetWizardConfig:
    symbol: str
    interval: str
    train_start_ms: int
    train_end_ms: int
    validation_end_ms: int
    test_end_ms: int

    def validate(self) -> None:
        if not self.train_start_ms < self.train_end_ms < self.validation_end_ms < self.test_end_ms:
            raise ValueError("dataset splits must be chronological")


@dataclass(frozen=True)
class CandidateModelPlan:
    alias: str
    dataset_id: str
    baseline_metric: str
    champion_auto_promote: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def save_candidate_plan(config: DatasetWizardConfig, plan: CandidateModelPlan, path: Path) -> Path:
    config.validate()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"dataset": asdict(config), "candidate": plan.to_dict(), "metrics": {"status": "planned"}}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def save_dataset_manifest_from_rows(
    *,
    dataset_id: str,
    source: str,
    config: DatasetWizardConfig,
    candles: list[Candle],
    features: list[FeatureRow],
    labels: list[LabelRow],
    lookback_window: int,
    label_horizon: int,
    path: Path,
    fee_bps: Decimal = Decimal("10"),
    slippage_bps: Decimal = Decimal("5"),
    spread_bps: Decimal = Decimal("0"),
) -> DatasetManifest:
    config.validate()
    train_rows = [
        row for row in features if config.train_start_ms <= row.timestamp_ms <= config.train_end_ms
    ]
    validation_rows = [
        row for row in features if config.train_end_ms < row.timestamp_ms <= config.validation_end_ms
    ]
    test_rows = [
        row for row in features if config.validation_end_ms < row.timestamp_ms <= config.test_end_ms
    ]
    manifest = build_dataset_manifest(
        dataset_id=dataset_id,
        source=source,
        symbol=config.symbol,
        interval=config.interval,
        candles=candles,
        features=features,
        labels=labels,
        train_rows=train_rows,
        validation_rows=validation_rows,
        test_rows=test_rows,
        lookback_window=lookback_window,
        label_horizon=label_horizon,
        fee_bps=fee_bps,
        slippage_bps=slippage_bps,
        spread_bps=spread_bps,
    )
    manifest.save(path)
    return manifest

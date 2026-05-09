from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


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

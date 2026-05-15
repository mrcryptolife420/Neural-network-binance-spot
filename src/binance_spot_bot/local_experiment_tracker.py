from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class ExperimentRun:
    run_id: str
    experiment_name: str
    status: str
    config: dict[str, Any]
    metrics: dict[str, Any] = field(default_factory=dict)
    artifacts: dict[str, str] = field(default_factory=dict)
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class LocalExperimentTracker:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.runs_dir = self.root / "runs"
        self.index_path = self.root / "experiment-runs.json"
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    def start_run(self, experiment_name: str, config: dict[str, Any]) -> ExperimentRun:
        run = ExperimentRun(f"train-{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}", experiment_name, "running", config)
        return self.save(run)

    def complete_run(self, run: ExperimentRun, *, metrics: dict[str, Any], artifacts: dict[str, str], status: str = "completed") -> ExperimentRun:
        return self.save(ExperimentRun(run.run_id, run.experiment_name, status, run.config, metrics, artifacts, run.created_at_ms))

    def save(self, run: ExperimentRun) -> ExperimentRun:
        path = self.runs_dir / f"{run.run_id}.json"
        path.write_text(json.dumps(run.to_dict(), indent=2, sort_keys=True, default=str), encoding="utf-8")
        rows = [item for item in self.list_runs() if item.run_id != run.run_id]
        rows.append(run)
        self.index_path.write_text(json.dumps([item.to_dict() for item in rows], indent=2, sort_keys=True, default=str), encoding="utf-8")
        return run

    def list_runs(self) -> list[ExperimentRun]:
        if not self.index_path.exists():
            return []
        payload = json.loads(self.index_path.read_text(encoding="utf-8"))
        return [ExperimentRun(**row) for row in payload]


def experiment_tracker(rows: int = 0) -> dict[str, Any]:
    status = "ok" if rows >= 0 else "blocked"
    return {"status": status, "rows": rows, "feature_contract": "local-paper-v1", "live_trading_enabled": False}

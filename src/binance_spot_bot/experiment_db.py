from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class ExperimentRecord:
    experiment_id: str
    kind: str
    artifact_path: str
    metrics: dict[str, Any]
    created_at_ms: int

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class ExperimentDB:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def add(self, kind: str, artifact_path: str, metrics: dict[str, Any] | None = None) -> ExperimentRecord:
        record = ExperimentRecord(f"exp-{int(time.time() * 1000)}", kind, artifact_path, metrics or {}, int(time.time() * 1000))
        rows = self.list()
        rows.append(record)
        self.path.write_text(json.dumps([row.to_dict() for row in rows], indent=2, default=str), encoding="utf-8")
        return record

    def list(self) -> list[ExperimentRecord]:
        if not self.path.exists():
            return []
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return [ExperimentRecord(**item) for item in payload]

    def index_sessions(self, sessions_root: Path) -> list[ExperimentRecord]:
        records = []
        for summary in sessions_root.glob("*/summary.json"):
            records.append(self.add("session", str(summary), {"indexed": True}))
        return records

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .experiment_db import ExperimentDB
from .redaction import redact_payload


@dataclass(frozen=True)
class ScannerRow:
    symbol: str
    spread_bps: float
    volume: float
    signal: str
    confidence: float

    def score(self) -> float:
        return self.confidence - (self.spread_bps / 1000.0) + min(self.volume, 1_000_000.0) / 10_000_000.0

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["score"] = self.score()
        return payload


def rank_watchlist(rows: list[ScannerRow]) -> list[ScannerRow]:
    return sorted(rows, key=lambda row: row.score(), reverse=True)


class ScannerHistory:
    def __init__(self, path: Path, experiments: ExperimentDB | None = None):
        self.path = path
        self.experiments = experiments
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record_run(self, rows: list[ScannerRow]) -> dict[str, Any]:
        payload = {"created_at_ms": int(time.time() * 1000), "rows": [row.to_dict() for row in rank_watchlist(rows)], "orders_allowed": False}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(redact_payload(payload), sort_keys=True) + "\n")
        if self.experiments:
            self.experiments.add("scanner", str(self.path), {"rows": len(rows), "orders_allowed": False})
        return payload

    def list_runs(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]

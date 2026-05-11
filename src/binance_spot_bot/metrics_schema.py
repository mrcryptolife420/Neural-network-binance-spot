from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any

from .redaction import redact_payload

METRIC_SCHEMA_VERSION = "1.0"
METRIC_CATEGORIES = {
    "job",
    "scheduler",
    "report",
    "health",
    "check",
    "dashboard",
    "session",
    "paper_performance",
    "portfolio",
    "governance",
    "support",
    "storage",
    "evidence",
    "data_quality",
    "incident",
}


@dataclass(frozen=True)
class MetricLabel:
    key: str
    value: str

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class MetricPoint:
    timestamp_ms: int
    value: float
    status: str = "ok"

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class MetricSeries:
    name: str
    labels: dict[str, str]
    points: list[MetricPoint]
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class MetricEvent:
    name: str
    value: float
    source: str = "local"
    category: str = "health"
    unit: str = "count"
    status: str = "ok"
    severity: str = "info"
    labels: dict[str, str] = field(default_factory=dict)
    artifact_path: str = ""
    evidence_id: str = ""
    timestamp_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    event_id: str = ""
    schema_version: str = METRIC_SCHEMA_VERSION
    redacted: bool = True
    live_trading_enabled: bool = False

    @property
    def ts_ms(self) -> int:
        return self.timestamp_ms

    def __post_init__(self) -> None:
        if self.category not in METRIC_CATEGORIES:
            raise ValueError("invalid metric category")
        if self.live_trading_enabled:
            raise ValueError("metrics cannot enable live trading")
        if not self.event_id:
            object.__setattr__(self, "event_id", f"{self.source}-{self.name}-{self.timestamp_ms}")

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MetricEvent":
        data = dict(payload)
        if "ts_ms" in data and "timestamp_ms" not in data:
            data["timestamp_ms"] = data.pop("ts_ms")
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{key: value for key, value in data.items() if key in allowed})


@dataclass(frozen=True)
class MetricIngestResult:
    status: str
    accepted: int
    rejected: int = 0
    reasons: list[str] = field(default_factory=list)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class MetricAggregation:
    name: str
    category: str
    period: str
    count: int
    min_value: float
    max_value: float
    avg_value: float
    status: str = "ok"
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class MetricAnomaly:
    name: str
    severity: str
    reason: str
    value: float | None = None
    recommended_action: str = "review_local_runbook"
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))

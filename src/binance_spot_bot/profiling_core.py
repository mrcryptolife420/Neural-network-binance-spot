from __future__ import annotations

import contextlib
import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterator

from .redaction import redact_payload


@dataclass
class ProfileSpan:
    span_id: str
    name: str
    category: str
    started_at_ms: float
    parent_span_id: str = ""
    duration_ms: float = 0.0
    status: str = "running"
    labels: dict[str, Any] = field(default_factory=dict)
    error_type: str = ""
    redacted: bool = True
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class ProfileMetric:
    name: str
    value: float
    unit: str
    labels: dict[str, Any] = field(default_factory=dict)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass
class ProfileRun:
    run_id: str
    category: str
    spans: list[ProfileSpan] = field(default_factory=list)
    metrics: list[ProfileMetric] = field(default_factory=list)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(
            {
                "run_id": self.run_id,
                "category": self.category,
                "spans": [span.to_dict() for span in self.spans],
                "metrics": [metric.to_dict() for metric in self.metrics],
                "live_trading_enabled": False,
            }
        )


@dataclass(frozen=True)
class ProfileBudget:
    budget_id: str
    category: str
    max_ms: float
    severity: str = "warn"
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProfileBudgetResult:
    budget_id: str
    measured_value: float
    budget_value: float
    status: str
    severity: str
    reason: str
    suggested_action: str
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def now_monotonic_ms() -> float:
    return time.perf_counter() * 1000.0


def start_span(name: str, category: str = "unknown", labels: dict[str, Any] | None = None, parent_span_id: str = "") -> ProfileSpan:
    return ProfileSpan(str(uuid.uuid4())[:12], name, category, now_monotonic_ms(), parent_span_id=parent_span_id, labels=labels or {})


def finish_span(span: ProfileSpan, status: str = "ok", error_type: str = "") -> ProfileSpan:
    span.duration_ms = max(0.0, now_monotonic_ms() - span.started_at_ms)
    span.status = status
    span.error_type = error_type
    return span


@contextlib.contextmanager
def profile_block(name: str, category: str = "unknown", labels: dict[str, Any] | None = None, run: ProfileRun | None = None) -> Iterator[ProfileSpan]:
    span = start_span(name, category, labels)
    try:
        yield span
    except Exception as exc:
        finish_span(span, "error", exc.__class__.__name__)
        if run is not None:
            run.spans.append(span)
        raise
    else:
        finish_span(span)
        if run is not None:
            run.spans.append(span)


def summarize_profile_run(run: ProfileRun | dict[str, Any]) -> dict[str, Any]:
    payload = run.to_dict() if isinstance(run, ProfileRun) else run
    spans = payload.get("spans", [])
    durations = [float(span.get("duration_ms", 0.0)) for span in spans]
    slowest = sorted(spans, key=lambda span: float(span.get("duration_ms", 0.0)), reverse=True)[:10]
    return redact_payload(
        {
            "status": "ready",
            "run_id": payload.get("run_id", ""),
            "category": payload.get("category", "unknown"),
            "span_count": len(spans),
            "total_duration_ms": round(sum(durations), 3),
            "max_duration_ms": round(max(durations, default=0.0), 3),
            "slowest_spans": slowest,
            "live_trading_enabled": False,
        }
    )


def redact_profile_payload(payload: Any) -> Any:
    return redact_payload(payload)


def write_profile_run(run: ProfileRun | dict[str, Any], out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    payload = run.to_dict() if isinstance(run, ProfileRun) else redact_payload(run)
    path = out / f"{payload.get('run_id', 'profile-run')}.json"
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    summary = summarize_profile_run(payload)
    summary_path = out / f"{payload.get('run_id', 'profile-run')}-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    return {"status": "ready", "path": str(path), "summary_path": str(summary_path), "summary": summary, "live_trading_enabled": False}

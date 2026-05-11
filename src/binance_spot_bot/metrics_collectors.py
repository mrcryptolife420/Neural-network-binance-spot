from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .metrics_schema import MetricEvent


def collect_artifact_metrics(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {"status": "ready", "events": [event.to_dict() for event in _artifact_events(items)], "artifact_count": len(items), "live_trading_enabled": False}


def collect_check_all_metrics(path: Path) -> list[MetricEvent]:
    payload = _load_json(path)
    status = payload.get("status", "missing")
    checks = payload.get("checks", [])
    return [
        MetricEvent("check_all.status", 1.0 if status == "ok" else 0.0, source="check-all", category="check", status=status),
        MetricEvent("check_all.failed_checks", float(sum(1 for row in checks if row.get("status") not in {"ok", "passed"})), source="check-all", category="check", status=status),
    ]


def collect_dashboard_smoke_metrics(path: Path) -> list[MetricEvent]:
    payload = _load_json(path)
    status = payload.get("status", "missing")
    return [
        MetricEvent("dashboard.smoke_status", 1.0 if status == "ok" else 0.0, source="dashboard-smoke", category="dashboard", status=status),
        MetricEvent("dashboard.smoke_checks", float(len(payload.get("checks", []))), source="dashboard-smoke", category="dashboard", status=status),
    ]


def collect_support_bundle_metrics(path: Path) -> list[MetricEvent]:
    payload = _load_json(path)
    return [MetricEvent("support.bundle_files", float(payload.get("files", 0)), source="support-bundle", category="support", artifact_path=str(path))]


def collect_data_growth_metrics(payload: dict[str, Any]) -> list[MetricEvent]:
    return [MetricEvent("storage.bytes", float(payload.get("total_bytes", payload.get("bytes", 0))), source="data-growth", category="storage", unit="bytes")]


def collect_evidence_metrics(payload: dict[str, Any]) -> list[MetricEvent]:
    status = payload.get("status", "ok")
    return [MetricEvent("evidence.items", float(len(payload.get("items", payload.get("files", [])))), source="evidence", category="evidence", status=status)]


def collect_local_job_metrics(runs: list[dict[str, Any]]) -> list[MetricEvent]:
    events = [MetricEvent("local_job.runs", float(len(runs)), source="local-jobs", category="job")]
    events.append(MetricEvent("local_job.failures", float(sum(1 for run in runs if run.get("status") not in {"ok", "ready"})), source="local-jobs", category="job"))
    return events


def missing_artifact_metric(name: str, path: Path) -> MetricEvent:
    return MetricEvent(name, 0.0, source="collector", category="evidence", status="missing", severity="warning", artifact_path=str(path))


def _artifact_events(items: list[dict[str, Any]]) -> list[MetricEvent]:
    total_bytes = sum(float(item.get("bytes", item.get("size", 0))) for item in items)
    return [
        MetricEvent("artifact.count", float(len(items)), source="artifact-catalog", category="evidence"),
        MetricEvent("artifact.bytes", total_bytes, source="artifact-catalog", category="storage", unit="bytes"),
    ]


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "missing", "timestamp_ms": int(time.time() * 1000)}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"status": "invalid"}
    return payload if isinstance(payload, dict) else {"status": "invalid"}

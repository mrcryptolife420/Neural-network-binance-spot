from __future__ import annotations

import time
from typing import Any

from .metrics_schema import MetricEvent


def local_ops_metric_snapshot(jobs: list[dict[str, Any]], runs: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    runs = runs or []
    failures = [run for run in runs if run.get("status") not in {"ok", "ready"}]
    stale = [job for job in jobs if int(job.get("last_success_ms", 0) or 0) and int(time.time() * 1000) - int(job.get("last_success_ms", 0)) > 86_400_000]
    events = [
        MetricEvent("local_ops.jobs", float(len(jobs)), source="local-ops", category="job"),
        MetricEvent("local_ops.runs", float(len(runs)), source="local-ops", category="job"),
        MetricEvent("local_ops.failures", float(len(failures)), source="local-ops", category="job", status="warn" if failures else "ok"),
        MetricEvent("local_ops.stale_jobs", float(len(stale)), source="local-ops", category="scheduler", status="warn" if stale else "ok"),
    ]
    return {"status": "warn" if failures or stale else "ok", "events": [event.to_dict() for event in events], "jobs": len(jobs), "failures": len(failures), "live_trading_enabled": False}

from __future__ import annotations

import statistics
import time
from typing import Any


def detect_metric_anomalies(rows: list[dict[str, Any]], *, stale_after_ms: int = 86_400_000) -> dict[str, Any]:
    anomalies: list[dict[str, Any]] = []
    values = [float(row.get("value", row.get("val", 0))) for row in rows]
    if any(value < 0 for value in values):
        anomalies.append({"severity": "warning", "reason": "negative_metric_value", "recommended_action": "review_operator_report"})
    failures = [row for row in rows if row.get("status") in {"failed", "blocked", "error"}]
    if len(failures) >= 2:
        anomalies.append({"severity": "critical", "reason": "failure_spike", "recommended_action": "open_failed_scheduled_report_runbook"})
    if values and len(values) >= 3:
        avg = statistics.mean(values[:-1])
        if avg and abs(values[-1] - avg) / abs(avg) > 2:
            anomalies.append({"severity": "warning", "reason": "rolling_average_deviation", "recommended_action": "review_metric_series"})
    now = int(time.time() * 1000)
    stale = [row for row in rows if int(row.get("timestamp_ms", row.get("ts_ms", now))) < now - stale_after_ms]
    if stale:
        anomalies.append({"severity": "warning", "reason": "stale_metric", "recommended_action": "run_metrics_ingest"})
    return {"status": "warn" if anomalies else "ok", "payload": {"anomalies": anomalies}, "anomalies": anomalies, "live_trading_enabled": False}

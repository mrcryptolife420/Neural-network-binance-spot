from __future__ import annotations

import hashlib
import json
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import BotSettings
from .metrics_schema import MetricAggregation, MetricEvent, MetricIngestResult
from .redaction import redact_payload


class MetricsWarehouse:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "metrics.jsonl"

    def append(self, metric: dict[str, Any] | MetricEvent) -> dict[str, Any]:
        event = metric if isinstance(metric, MetricEvent) else _event_from_legacy(metric)
        legacy_numeric = {
            key: value
            for key, value in (metric.items() if isinstance(metric, dict) else [])
            if isinstance(value, int | float) and key not in {"timestamp_ms", "ts_ms", "value"}
        }
        payload = redact_payload({**event.to_dict(), **legacy_numeric, "live_trading_enabled": False})
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, default=str) + "\n")
        return payload

    def append_metric(self, event: MetricEvent) -> MetricIngestResult:
        self.append(event)
        return MetricIngestResult("ok", 1)

    def append_many(self, events: list[MetricEvent]) -> MetricIngestResult:
        for event in events:
            self.append(event)
        return MetricIngestResult("ok", len(events))

    def load(self, limit: int = 500) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        rows = [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
        return rows[-limit:]

    def query_metrics(
        self,
        *,
        name: str | None = None,
        category: str | None = None,
        since_ms: int | None = None,
        labels: dict[str, str] | None = None,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        rows = self.load(limit=10_000)
        result = []
        for row in rows:
            if name and row.get("name") != name:
                continue
            if category and row.get("category") != category:
                continue
            if since_ms and int(row.get("timestamp_ms", row.get("ts_ms", 0))) < since_ms:
                continue
            row_labels = row.get("labels", {})
            if labels and any(str(row_labels.get(k)) != str(v) for k, v in labels.items()):
                continue
            result.append(row)
        return result[-limit:]

    def latest_metric(self, name: str) -> dict[str, Any] | None:
        rows = self.query_metrics(name=name, limit=1)
        return rows[-1] if rows else None

    def series(self, name: str, labels: dict[str, str] | None = None, since_ms: int | None = None) -> dict[str, Any]:
        rows = self.query_metrics(name=name, labels=labels, since_ms=since_ms)
        return {"name": name, "labels": labels or {}, "points": [{"timestamp_ms": row["timestamp_ms"], "value": row["value"]} for row in rows], "live_trading_enabled": False}

    def aggregate_daily(self) -> dict[str, Any]:
        return _write_aggregate(self.root / "daily", "daily", self.load(limit=100_000))

    def aggregate_weekly(self) -> dict[str, Any]:
        return _write_aggregate(self.root / "weekly", "weekly", self.load(limit=100_000))

    def write_manifest(self) -> Path:
        manifests = self.root / "manifests"
        manifests.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(self.path.read_bytes()).hexdigest() if self.path.exists() else ""
        parts = [digest[index : index + 16] for index in range(0, len(digest), 16)] if digest else []
        payload = {"metrics_file": self.path.name, "sha256": f"{parts[0]}...{parts[-1]}" if parts else "", "sha256_parts": parts, "bytes": self.path.stat().st_size if self.path.exists() else 0, "live_trading_enabled": False}
        path = manifests / "metrics-manifest.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def verify_manifest(self, manifest_path: Path | None = None) -> dict[str, Any]:
        path = manifest_path or self.root / "manifests" / "metrics-manifest.json"
        if not path.exists():
            return {"status": "missing", "live_trading_enabled": False}
        payload = json.loads(path.read_text(encoding="utf-8"))
        expected = "".join(payload.get("sha256_parts", []))
        actual = hashlib.sha256(self.path.read_bytes()).hexdigest() if self.path.exists() else ""
        return {"status": "ok" if expected == actual else "failed", "live_trading_enabled": False}

    def compact_old_metrics(self, *, keep_latest: int = 1000, confirm: str = "") -> dict[str, Any]:
        rows = self.load(limit=100_000)
        archive_count = max(0, len(rows) - keep_latest)
        if confirm != "COMPACT_METRICS":
            return {"status": "preview", "archive_count": archive_count, "live_trading_enabled": False}
        kept = rows[-keep_latest:]
        self.path.write_text("\n".join(json.dumps(row, default=str) for row in kept) + ("\n" if kept else ""), encoding="utf-8")
        self.write_manifest()
        return {"status": "compacted", "archive_count": archive_count, "kept": len(kept), "live_trading_enabled": False}


def aggregate_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    numeric: dict[str, list[float]] = {}
    normalized = [_normalize_row(row) for row in rows]
    for row in normalized:
        name = row.get("name")
        value = row.get("value")
        if name and isinstance(value, int | float):
            numeric.setdefault(str(name), []).append(float(value))
        for key, item in row.items():
            if isinstance(item, bool):
                continue
            if isinstance(item, int | float) and key not in {"timestamp_ms", "ts_ms", "value"}:
                numeric.setdefault(key, []).append(float(item))
    aggregates = {
        key: {"avg": round(statistics.mean(values), 6), "min": min(values), "max": max(values), "count": len(values)}
        for key, values in sorted(numeric.items())
    }
    anomalies = [
        {"metric": key, "reason": "negative_equity_or_pnl", "value": stats["min"], "recommended_action": "review_operator_report"}
        for key, stats in aggregates.items()
        if key in {"equity", "pnl_quote", "paper.pnl"} and stats["min"] < 0
    ]
    status = "warn" if anomalies else "ok"
    return {"status": status, "metrics": aggregates, "anomalies": anomalies, "rows": len(rows), "live_trading_enabled": False}


def write_metrics_report(settings: BotSettings, rows: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    warehouse = MetricsWarehouse(settings.data_dir / "metrics-warehouse")
    if rows is not None:
        for row in rows:
            warehouse.append(row)
    loaded = warehouse.load()
    summary = aggregate_metrics(loaded)
    manifest = warehouse.write_manifest()
    out = settings.data_dir / "metrics-warehouse" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "latest-metrics-report.json"
    md_path = out / "latest-metrics-report.md"
    json_path.write_text(json.dumps(redact_payload(summary), indent=2, default=str), encoding="utf-8")
    md_path.write_text(_report_markdown(summary, manifest), encoding="utf-8")
    return {"paths": {"json": str(json_path), "markdown": str(md_path), "manifest": str(manifest)}, **summary}


def _event_from_legacy(metric: dict[str, Any]) -> MetricEvent:
    payload = redact_payload(metric)
    name = str(payload.get("name", payload.get("metric", "legacy.metric")))
    if "pnl_quote" in payload:
        name = "pnl_quote"
    value = payload.get("value", payload.get("pnl_quote", payload.get("equity", 0.0)))
    try:
        value_float = float(value)
    except (TypeError, ValueError):
        value_float = 0.0
    return MetricEvent(
        name=name,
        value=value_float,
        source=str(payload.get("source", "legacy")),
        category=str(payload.get("category", "health")),
        unit=str(payload.get("unit", "count")),
        status=str(payload.get("status", "ok")),
        severity=str(payload.get("severity", "info")),
        labels={str(k): str(v) for k, v in dict(payload.get("labels", {})).items()},
        artifact_path=str(payload.get("artifact_path", "")),
        evidence_id=str(payload.get("evidence_id", "")),
        timestamp_ms=int(payload.get("timestamp_ms", payload.get("ts_ms", int(time.time() * 1000)))),
    )


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    if "timestamp_ms" not in row and "ts_ms" in row:
        row = {**row, "timestamp_ms": row["ts_ms"]}
    return row


def _write_aggregate(root: Path, period: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    summary = aggregate_metrics(rows)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d" if period == "daily" else "%Y-W%V")
    path = root / f"{stamp}.json"
    path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    return {"status": summary["status"], "period": period, "path": str(path), **summary}


def _report_markdown(summary: dict[str, Any], manifest: Path) -> str:
    return "\n".join(
        [
            "# Local Paper Metrics Warehouse",
            "",
            "LOCAL OBSERVABILITY ONLY",
            f"Status: {summary['status']}",
            f"Rows: {summary['rows']}",
            f"Anomalies: {len(summary['anomalies'])}",
            f"Manifest: {manifest}",
            "Live trading: disabled",
            "",
        ]
    )

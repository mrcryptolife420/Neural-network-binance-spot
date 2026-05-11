from __future__ import annotations

import json
import statistics
import time
from pathlib import Path
from typing import Any

from .config import BotSettings
from .redaction import redact_payload


class MetricsWarehouse:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "metrics.jsonl"

    def append(self, metric: dict[str, Any]) -> dict[str, Any]:
        payload = redact_payload({"ts_ms": int(time.time() * 1000), **metric, "live_trading_enabled": False})
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, default=str) + "\n")
        return payload

    def load(self, limit: int = 500) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        rows = [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
        return rows[-limit:]


def aggregate_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    numeric: dict[str, list[float]] = {}
    for row in rows:
        for key, value in row.items():
            if isinstance(value, int | float) and key != "ts_ms":
                numeric.setdefault(key, []).append(float(value))
    aggregates = {
        key: {"avg": round(statistics.mean(values), 6), "min": min(values), "max": max(values), "count": len(values)}
        for key, values in numeric.items()
    }
    anomalies = [
        {"metric": key, "reason": "negative_equity_or_pnl", "value": stats["min"]}
        for key, stats in aggregates.items()
        if key in {"equity", "pnl_quote"} and stats["min"] < 0
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
    out = settings.data_dir / "metrics-warehouse" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "latest-metrics-report.json"
    md_path = out / "latest-metrics-report.md"
    json_path.write_text(json.dumps(redact_payload(summary), indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Local Paper Metrics Warehouse",
                "",
                f"Status: {summary['status']}",
                f"Rows: {summary['rows']}",
                f"Anomalies: {len(summary['anomalies'])}",
                "Live trading: disabled",
            ]
        ),
        encoding="utf-8",
    )
    return {"paths": {"json": str(json_path), "markdown": str(md_path)}, **summary}

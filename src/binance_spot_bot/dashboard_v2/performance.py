from __future__ import annotations

from pathlib import Path
from typing import Any

from .performance_baseline import write_dashboard_v2_performance_report


def dashboard_v2_performance_report(root: Path | str = ".") -> dict[str, Any]:
    baseline = write_dashboard_v2_performance_report(root)
    report = baseline["report"]
    payload = {
        "status": "ok",
        "metrics": {sample["name"]: sample["value"] for sample in report["baseline"]["samples"]},
        "budgets": {"snapshot_payload_bytes": 500_000, "api_snapshot_ms": 500, "chart_update_ms": 120},
        "baseline": baseline,
        "no_live_statement": report["baseline"]["no_live_statement"],
        "live_trading_enabled": False,
    }
    out = Path(root) / "data" / "dashboard-v2" / "performance"
    out.mkdir(parents=True, exist_ok=True)
    (out / "dashboard_v2_performance.json").write_text(__import__("json").dumps(payload, indent=2), encoding="utf-8")
    (out / "dashboard_v2_performance.md").write_text(
        f"# Dashboard V2 Performance\n\nStatus: {payload['status']}\nLive trading: disabled\n",
        encoding="utf-8",
    )
    return payload

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


MetricProbe = Callable[[], float | int | None]


@dataclass(frozen=True)
class DashboardV2PerformanceSample:
    name: str
    value: float | int | None
    unit: str = "ms"
    status: str = "ok"
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


@dataclass(frozen=True)
class DashboardV2PerformanceBaseline:
    samples: list[DashboardV2PerformanceSample]
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False
    generated_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


@dataclass(frozen=True)
class DashboardV2PerformanceReport:
    status: str
    baseline: DashboardV2PerformanceBaseline
    browser_console_errors: int = 0
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


DEFAULT_METRICS: tuple[tuple[str, str], ...] = (
    ("backend_startup_ms", "ms"),
    ("api_health_ms", "ms"),
    ("api_config_ms", "ms"),
    ("api_pages_ms", "ms"),
    ("api_snapshot_ms", "ms"),
    ("websocket_connect_ms", "ms"),
    ("websocket_heartbeat_ms", "ms"),
    ("snapshot_serialization_ms", "ms"),
    ("snapshot_payload_bytes", "bytes"),
    ("frontend_initial_load_ms", "ms"),
    ("route_navigation_ms", "ms"),
    ("chart_update_ms", "ms"),
    ("memory_best_effort_mb", "mb"),
    ("cpu_best_effort_pct", "pct"),
)


def measure_dashboard_v2_baseline(
    samples: dict[str, float | int | None] | None = None,
    probes: dict[str, MetricProbe] | None = None,
    *,
    browser_console_errors: int = 0,
) -> DashboardV2PerformanceReport:
    sample_values = dict(samples or {})
    warnings: list[str] = []
    rows: list[DashboardV2PerformanceSample] = []
    probes = probes or {}
    for name, unit in DEFAULT_METRICS:
        value = sample_values.get(name)
        if value is None and name in probes:
            value = probes[name]()
        status = "ok" if value is not None else "unknown"
        note = "" if value is not None else "optional sample missing"
        if note:
            warnings.append(f"{name}: {note}")
        rows.append(DashboardV2PerformanceSample(name=name, value=value, unit=unit, status=status, note=note))
    baseline = DashboardV2PerformanceBaseline(samples=rows, warnings=warnings)
    recommendations = ["Collect missing optional browser/static metrics"] if warnings else []
    if browser_console_errors:
        recommendations.append("Resolve browser console errors before cutover")
    return DashboardV2PerformanceReport(
        status="warn" if warnings or browser_console_errors else "ok",
        baseline=baseline,
        browser_console_errors=browser_console_errors,
        recommendations=recommendations,
    )


def dashboard_v2_performance_report_to_dict(report: DashboardV2PerformanceReport) -> dict[str, Any]:
    return report.to_dict()


def write_dashboard_v2_performance_report(root: Path | str, report: DashboardV2PerformanceReport | None = None) -> dict[str, Any]:
    root = Path(root)
    report = report or measure_dashboard_v2_baseline()
    out = root / "data" / "dashboard-v2" / "performance"
    out.mkdir(parents=True, exist_ok=True)
    payload = dashboard_v2_performance_report_to_dict(report)
    json_path = out / "baseline.json"
    md_path = out / "baseline.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    rows = payload["baseline"]["samples"]
    lines = [
        "# Dashboard V2 Performance Baseline",
        "",
        f"Status: {payload['status']}",
        f"No-live proof: {payload['baseline']['no_live_statement']}",
        "",
        "| Metric | Value | Unit | Status |",
        "| --- | ---: | --- | --- |",
    ]
    lines.extend(f"| {row['name']} | {row['value']} | {row['unit']} | {row['status']} |" for row in rows)
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return redact_dashboard_payload({"status": payload["status"], "json": str(json_path), "markdown": str(md_path), "report": payload})

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .performance_baseline import DashboardV2PerformanceReport, measure_dashboard_v2_baseline
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


DEFAULT_BUDGETS: dict[str, float] = {
    "backend_startup_ms": 2500,
    "api_health_ms": 100,
    "api_config_ms": 150,
    "api_pages_ms": 250,
    "api_snapshot_ms": 500,
    "snapshot_payload_bytes": 500_000,
    "websocket_connect_ms": 500,
    "frontend_initial_load_ms": 2500,
    "route_navigation_ms": 500,
    "chart_update_ms": 120,
}


@dataclass(frozen=True)
class DashboardV2BudgetResult:
    metric: str
    status: str
    value: float | int | None
    budget: float | None
    recommendation: str = ""


@dataclass(frozen=True)
class DashboardV2BudgetReport:
    status: str
    results: list[DashboardV2BudgetResult]
    hard_blockers: list[str] = field(default_factory=list)
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


def evaluate_dashboard_v2_performance_budgets(
    report: DashboardV2PerformanceReport | None = None,
    budgets: dict[str, float] | None = None,
) -> DashboardV2BudgetReport:
    report = report or measure_dashboard_v2_baseline()
    budgets = budgets or DEFAULT_BUDGETS
    payload = report.to_dict()
    hard_blockers: list[str] = []
    if payload["baseline"].get("live_trading_enabled") is not False:
        hard_blockers.append("live trading flag must be false")
    if not payload["baseline"].get("no_live_statement"):
        hard_blockers.append("no-live proof missing")
    rows: list[DashboardV2BudgetResult] = []
    for sample in payload["baseline"]["samples"]:
        metric = sample["name"]
        value = sample["value"]
        budget = budgets.get(metric)
        if value is None:
            status = "unknown"
            recommendation = "collect metric before cutover"
        elif budget is None:
            status = "skipped"
            recommendation = ""
        elif float(value) <= budget:
            status = "pass"
            recommendation = ""
        elif float(value) <= budget * 1.25:
            status = "warn"
            recommendation = "optimize before release package"
        else:
            status = "fail"
            recommendation = "blocks Dashboard V2 cutover"
        rows.append(DashboardV2BudgetResult(metric=metric, value=value, budget=budget, status=status, recommendation=recommendation))
    browser_errors = int(payload.get("browser_console_errors", 0))
    rows.append(
        DashboardV2BudgetResult(
            metric="browser_console_errors",
            value=browser_errors,
            budget=0,
            status="pass" if browser_errors == 0 else "fail",
            recommendation="" if browser_errors == 0 else "fix fatal frontend console errors",
        )
    )
    statuses = {row.status for row in rows}
    status = "blocked" if hard_blockers or "fail" in statuses else "warn" if statuses & {"warn", "unknown"} else "ok"
    return DashboardV2BudgetReport(status=status, results=rows, hard_blockers=hard_blockers)


def write_dashboard_v2_budget_report(root: Path | str, report: DashboardV2BudgetReport | None = None) -> dict[str, Any]:
    root = Path(root)
    report = report or evaluate_dashboard_v2_performance_budgets()
    out = root / "data" / "dashboard-v2" / "performance"
    out.mkdir(parents=True, exist_ok=True)
    payload = report.to_dict()
    json_path = out / "budget.json"
    md_path = out / "budget.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = ["# Dashboard V2 Performance Budget", "", f"Status: {payload['status']}", ""]
    lines.extend(f"- {row['metric']}: {row['status']} ({row['value']} <= {row['budget']})" for row in payload["results"])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return redact_dashboard_payload({"status": payload["status"], "json": str(json_path), "markdown": str(md_path), "report": payload})

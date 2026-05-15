from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_BUDGETS = {
    "runtime_step_ms": 250.0,
    "dashboard_import_ms": 3000.0,
    "dashboard_panel_ms": 750.0,
    "cli_command_ms": 5000.0,
    "check_all_ms": 300000.0,
    "memory_peak_mb": 1024.0,
    "artifact_size_bytes": 50_000_000.0,
}


def load_performance_budgets(path: Path | str | None = None) -> dict[str, Any]:
    if path and Path(path).exists():
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("budget must be object")
            return {"status": "ready", "budgets": {**DEFAULT_BUDGETS, **data}, "live_trading_enabled": False}
        except Exception as exc:
            return {"status": "fallback", "reason": exc.__class__.__name__, "budgets": DEFAULT_BUDGETS, "live_trading_enabled": False}
    return {"status": "ready", "budgets": DEFAULT_BUDGETS, "live_trading_enabled": False}


def evaluate_performance_budget(metric: str, measured_value: float, budgets: dict[str, float] | None = None) -> dict[str, Any]:
    budget_map = budgets or DEFAULT_BUDGETS
    budget = float(budget_map.get(metric, measured_value))
    ratio = measured_value / budget if budget else 0
    status = "ok" if measured_value <= budget else "warn" if ratio <= 1.25 else "fail"
    return {
        "status": status,
        "budget_id": metric,
        "category": metric,
        "measured_value": measured_value,
        "budget_value": budget,
        "severity": "error" if status == "fail" else "warning" if status == "warn" else "info",
        "reason": "within budget" if status == "ok" else "budget exceeded",
        "suggested_action": "profile slow path" if status != "ok" else "none",
        "live_trading_enabled": False,
    }


def performance_budget(actual_ms: float, budget_ms: float) -> dict[str, Any]:
    status = "ok" if actual_ms <= budget_ms else "warn"
    return {"status": status, "actual_ms": actual_ms, "budget_ms": budget_ms, "live_trading_enabled": False}

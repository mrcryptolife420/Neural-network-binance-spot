from __future__ import annotations

from typing import Any


def detect_performance_regression(metric: str, previous_value: float | None, current_value: float, budget_value: float | None = None) -> dict[str, Any]:
    if previous_value is None:
        return {"status": "unknown", "regressions": [], "reason": "no_previous_history", "live_trading_enabled": False}
    delta = current_value - previous_value
    delta_pct = (delta / previous_value * 100.0) if previous_value else 0.0
    severity = "critical" if delta_pct > 50 else "warning" if delta_pct > 20 else "info"
    blocker = bool(budget_value is not None and current_value > budget_value and severity == "critical")
    regression = {
        "regression_id": metric,
        "metric": metric,
        "previous_value": previous_value,
        "current_value": current_value,
        "delta_abs": delta,
        "delta_pct": round(delta_pct, 3),
        "severity": severity,
        "likely_cause": "recent changed files or artifact growth",
        "recommended_tests": ["python -m pytest -q"] if severity != "info" else [],
        "recommended_refactor": "inspect slowest spans" if severity != "info" else "",
        "blockers": ["strict_budget_failed"] if blocker else [],
    }
    return {"status": "regression" if severity != "info" else "ok", "regressions": [regression] if severity != "info" else [], "live_trading_enabled": False}


def performance_regression(baseline_ms: float, cur_ms: float) -> dict[str, Any]:
    result = detect_performance_regression("duration_ms", baseline_ms, cur_ms)
    return {"status": result["status"], "payload": result, "live_trading_enabled": False}

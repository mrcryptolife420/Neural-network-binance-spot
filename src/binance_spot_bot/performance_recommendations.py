from __future__ import annotations

from typing import Any


def performance_recommendations(report: dict) -> dict[str, Any]:
    recommendations = []
    for span in report.get("slowest_spans", []):
        if span.get("category") == "dashboard":
            recommendations.append({"recommendation_id": "split_dashboard_panel", "target": span.get("name"), "evidence": span, "expected_impact": "lower render latency", "risk_level": "medium", "suggested_tests": ["dashboard-smoke", "dashboard-browser-smoke"], "no_live_constraints": True})
        elif float(span.get("duration_ms", 0)) > 1000:
            recommendations.append({"recommendation_id": "profile_slow_path", "target": span.get("name"), "evidence": span, "expected_impact": "identify bottleneck", "risk_level": "low", "suggested_tests": ["python -m pytest -q"], "no_live_constraints": True})
    if report.get("status") in {"warn", "fail", "regression"}:
        recommendations.append({"recommendation_id": "run_deep_profile_before_release", "target": "release", "evidence": report, "expected_impact": "avoid performance regression", "risk_level": "low", "suggested_tests": ["perf-regression-check"], "no_live_constraints": True})
    return {"status": "ready", "recommendations": recommendations, "live_trading_enabled": False}

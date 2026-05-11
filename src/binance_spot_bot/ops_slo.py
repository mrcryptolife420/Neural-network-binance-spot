from __future__ import annotations

from typing import Any


def evaluate_ops_slo(metrics: dict[str, Any]) -> dict[str, Any]:
    checks = [
        _rate_check("check_all_success_rate", float(metrics.get("check_all_success_rate", 1.0)), 0.95),
        _rate_check("dashboard_smoke_success_rate", float(metrics.get("dashboard_smoke_success_rate", 1.0)), 0.95),
        _freshness_check("daily_report_age_hours", float(metrics.get("daily_report_age_hours", 0.0)), 24.0),
        _freshness_check("weekly_governance_age_days", float(metrics.get("weekly_governance_age_days", 0.0)), 7.0),
        _rate_check("support_bundle_verify_rate", float(metrics.get("support_bundle_verify_rate", 1.0)), 0.99),
        _rate_check("redaction_self_test_rate", float(metrics.get("redaction_self_test_rate", 1.0)), 1.0),
        _freshness_check("evidence_manifest_age_hours", float(metrics.get("evidence_manifest_age_hours", 0.0)), 24.0),
        {"name": "no_live_trading_proof", "status": "ok" if metrics.get("live_trading_enabled", False) is False else "breach", "target": False, "actual": metrics.get("live_trading_enabled", False)},
    ]
    status = "breach" if any(row["status"] == "breach" for row in checks) else "warning" if any(row["status"] == "warning" for row in checks) else "ok"
    return {"status": status, "checks": checks, "recommended_action": "review_runbook" if status != "ok" else "none", "live_trading_enabled": False}


def _rate_check(name: str, actual: float, target: float) -> dict[str, Any]:
    return {"name": name, "status": "ok" if actual >= target else "breach", "target": target, "actual": actual}


def _freshness_check(name: str, actual: float, target: float) -> dict[str, Any]:
    return {"name": name, "status": "ok" if actual <= target else "breach", "target": target, "actual": actual}

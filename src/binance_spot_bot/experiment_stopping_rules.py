from __future__ import annotations

from typing import Any


def evaluate_stopping_rules(
    report: dict[str, Any],
    *,
    max_drawdown: float = 25.0,
    min_samples: int = 10,
    underperformance_ratio: float = 0.8,
    max_blocked_rate: float = 0.5,
    max_conflict_rate: float = 0.25,
    max_turnover: float = 1_000_000.0,
) -> dict[str, Any]:
    metrics = report.get("metrics", {})
    challenger = metrics.get("challenger", {})
    champion = metrics.get("champion", {})
    reasons: list[str] = []
    evidence_refs: list[str] = [str(report.get("experiment_id", report.get("rollout_id", "unknown")))]
    if float(challenger.get("drawdown", 0.0)) > max_drawdown:
        reasons.append("challenger_max_drawdown")
    if float(challenger.get("risk_adjusted_ret", 0.0)) < float(champion.get("risk_adjusted_ret", 0.0)) * underperformance_ratio:
        reasons.append("challenger_underperforms")
    if int(challenger.get("observations", 0)) < min_samples:
        reasons.append("too_few_samples")
    if int(challenger.get("policy_violations", 0)) > 0:
        reasons.append("policy_violation")
    if int(challenger.get("watchdog_alerts", 0)) > 0:
        reasons.append("watchdog_alert")
    if int(challenger.get("data_quality_warnings", 0)) > 0:
        reasons.append("data_quality_warning")
    if float(challenger.get("blocked_rate", 0.0)) > max_blocked_rate:
        reasons.append("blocked_rate_too_high")
    if float(challenger.get("conflict_rate", 0.0)) > max_conflict_rate:
        reasons.append("conflict_rate_too_high")
    if float(challenger.get("turnover", 0.0)) > max_turnover:
        reasons.append("turnover_too_high")
    if report.get("guardrails", {}).get("signed_endpoint_used", False):
        reasons.append("signed_endpoint_used")
    action = "pause_challenger" if reasons else "continue"
    return {
        "status": "stop" if reasons else "continue",
        "action": action,
        "reasons": sorted(set(reasons)),
        "evidence_refs": evidence_refs,
        "live_trading_enabled": False,
    }

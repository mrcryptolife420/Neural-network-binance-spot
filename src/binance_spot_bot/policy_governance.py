from __future__ import annotations

from typing import Any

GOVERNANCE_DECISIONS = {
    "keep_champion",
    "promote_challenger",
    "extend_experiment",
    "reduce_challenger",
    "rerun_experiment",
    "suspend_challenger",
    "archive_challenger",
    "rollback",
    "no_policy",
}


def governance_decision(
    experiment_report: dict[str, Any],
    stop_report: dict[str, Any],
    *,
    operator_confirmed: bool = False,
    sample_target: int = 1,
) -> dict[str, Any]:
    champion = experiment_report.get("metrics", {}).get("champion", {})
    challenger = experiment_report.get("metrics", {}).get("challenger", {})
    reasons: list[str] = []
    if not experiment_report:
        return _decision("no_policy", ["experiment_report_missing"], operator_confirmed)
    if stop_report.get("status") == "stop":
        reasons = list(stop_report.get("reasons", []))
        if any(reason in reasons for reason in ("policy_violation", "signed_endpoint_used", "watchdog_alert")):
            return _decision("suspend_challenger", reasons, operator_confirmed, stop_report.get("evidence_refs", []))
        return _decision("reduce_challenger", reasons, operator_confirmed, stop_report.get("evidence_refs", []))
    if int(challenger.get("observations", 0)) < sample_target:
        return _decision("extend_experiment", ["sample_target_not_met"], operator_confirmed)
    if experiment_report.get("decision") == "challenger_leads":
        if not operator_confirmed:
            return _decision("extend_experiment", ["operator_confirmation_required"], operator_confirmed)
        return _decision("promote_challenger", ["challenger_leads", "operator_confirmed", "paper_only"], operator_confirmed)
    if float(challenger.get("risk_adjusted_ret", 0.0)) < float(champion.get("risk_adjusted_ret", 0.0)) * 0.5:
        return _decision("archive_challenger", ["material_underperformance"], operator_confirmed)
    return _decision("keep_champion", ["champion_leads_or_equal"], operator_confirmed)


def _decision(
    decision: str,
    reasons: list[str],
    operator_confirmed: bool,
    evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    if decision not in GOVERNANCE_DECISIONS:
        raise ValueError("invalid governance decision")
    return {
        "decision": decision,
        "reasons": sorted(set(reasons)),
        "operator_confirmed": operator_confirmed,
        "evidence_refs": evidence_refs or [],
        "live_trading_enabled": False,
    }

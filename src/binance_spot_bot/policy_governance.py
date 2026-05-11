from __future__ import annotations

from typing import Any


def governance_decision(experiment_report: dict[str, Any], stop_report: dict[str, Any], *, operator_confirmed: bool = False) -> dict[str, Any]:
    if stop_report.get("status") == "stop":
        return {"decision": "suspend_challenger", "reasons": stop_report.get("reasons", []), "live_trading_enabled": False}
    if experiment_report.get("decision") == "challenger_leads" and operator_confirmed:
        return {"decision": "promote_challenger", "reasons": ["challenger_leads", "operator_confirmed"], "live_trading_enabled": False}
    if experiment_report.get("decision") == "challenger_leads":
        return {"decision": "extend_experiment", "reasons": ["operator_confirmation_required"], "live_trading_enabled": False}
    return {"decision": "keep_champion", "reasons": ["champion_leads_or_equal"], "live_trading_enabled": False}

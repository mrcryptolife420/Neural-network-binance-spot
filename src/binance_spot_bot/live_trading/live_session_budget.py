from __future__ import annotations

from typing import Any


def evaluate_live_session_budget(plan_report: dict[str, Any], usage: dict[str, Any]) -> dict[str, Any]:
    budget = plan_report.get("plan", {}).get("budget", {})
    risk = plan_report.get("plan", {}).get("risk", {})
    blockers = []
    warnings = []
    if int(usage.get("orders", 0)) >= int(budget.get("max_session_orders", 0)):
        blockers.append("max session orders reached")
    if float(usage.get("quote_exposure", 0)) > float(budget.get("max_session_quote_exposure", 0)):
        blockers.append("max quote exposure reached")
    if float(usage.get("single_order_quote", 0)) > float(budget.get("max_single_order_quote", 0)):
        blockers.append("max single order quote reached")
    if float(usage.get("session_loss_quote", 0)) >= float(budget.get("max_session_loss_quote", 0)):
        blockers.append("max session loss reached")
    if float(usage.get("spread_bps", 0)) > float(risk.get("max_spread_bps", 0)):
        blockers.append("max spread reached")
    if int(usage.get("data_age_ms", 0)) > int(risk.get("max_data_age_ms", 0)):
        blockers.append("stale market data")
    decision = "disarm" if blockers else "allow"
    return {"status": "blocked" if blockers else "ok", "decision": decision, "blockers": blockers, "warnings": warnings, "live_trading_enabled": False}

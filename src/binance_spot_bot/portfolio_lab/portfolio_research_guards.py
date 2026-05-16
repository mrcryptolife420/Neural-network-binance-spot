from __future__ import annotations

from typing import Any

from . import NO_LIVE_STATEMENT
from .candidate_basket import PortfolioCandidateBasket
from .common import has_advice_wording


def evaluate_portfolio_research_guards(
    basket: PortfolioCandidateBasket,
    allocation: dict[str, Any],
    risk_report: dict[str, Any] | None = None,
    stress_report: dict[str, Any] | None = None,
    correlation_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    active = [item for item in basket.items if not item.disabled and not item.blocked_reason]
    if len(active) < 2:
        blockers.append("too few candidates")
    if basket.no_live_statement != NO_LIVE_STATEMENT or basket.live_trading_enabled:
        blockers.append("missing no-live proof")
    if has_advice_wording({"basket": basket, "allocation": allocation}):
        blockers.append("advice wording violation")
    if risk_report and float(risk_report.get("concentration_score", 0.0)) > 0.55:
        blockers.append("overconcentration")
    if risk_report and float(risk_report.get("portfolio_max_drawdown", 0.0)) > 0.12:
        warnings.append("high drawdown allocation")
    if stress_report and stress_report.get("warnings"):
        warnings.append("stress test warning")
    if correlation_report and len(correlation_report.get("warnings", [])) > 2:
        warnings.append("correlation proxy warning")
    return {"status": "blocked" if blockers else ("warn" if warnings else "pass"), "blockers": blockers, "warnings": warnings, "live_trading_enabled": False}


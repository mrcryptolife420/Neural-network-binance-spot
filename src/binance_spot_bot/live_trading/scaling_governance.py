from __future__ import annotations

from typing import Any


def scaling_governance(current: int, target: int, grade: str, approved: bool):
    return {"decision": "approved_for_next_level" if approved and target == current + 1 and grade in {"A", "B"} else "blocked", "live_order_submitted": False, "live_trading_enabled": False}


def decide_live_scaling(current: int, target: int, scorecard: dict[str, Any], *, approved: bool, successful_sessions: int = 0, unresolved_findings: list[str] | None = None) -> dict[str, Any]:
    unresolved_findings = unresolved_findings or []
    blockers = []
    if target > current + 1:
        blockers.append("cannot skip scaling level")
    if successful_sessions < 1:
        blockers.append("minimum successful sessions required")
    if unresolved_findings:
        blockers.append("unresolved findings block promotion")
    if scorecard.get("grade") not in {"A", "B"}:
        blockers.append("latest session grade below threshold")
    if not approved:
        blockers.append("operator approval required")
    decision = "approved_for_next_level" if not blockers else ("demote_level" if scorecard.get("grade") in {"D", "F"} else "blocked")
    return {"status": "ok" if not blockers else "blocked", "decision": decision, "blockers": blockers, "auto_approved": False, "live_order_submitted": False, "live_trading_enabled": False}

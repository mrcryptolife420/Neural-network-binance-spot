from __future__ import annotations

from typing import Any

FORBIDDEN_ROTATION_ALIASES = {"champion_live", "live_approved", "auto_live", "live_portfolio", "live_allocation"}


def rotation_governance(score: float, confirm: bool, *, target_alias: str = "candidate", evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    blockers: list[str] = []
    if score < 0.6:
        blockers.append("score_below_rotation_threshold")
    if not confirm:
        blockers.append("operator_confirmation_required")
    if target_alias in FORBIDDEN_ROTATION_ALIASES:
        blockers.append("live_alias_forbidden")
    if evidence is None:
        blockers.append("evidence_required")
    return {"status": "approved" if not blockers else "blocked", "blockers": blockers, "target_alias": target_alias, "scope": "paper_shadow_demo_only", "live_trading_enabled": False}

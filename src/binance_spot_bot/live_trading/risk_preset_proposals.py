from __future__ import annotations


def risk_preset_proposal(kind: str):
    return {"status": "proposal", "kind": kind, "mutates_active_profile": False, "approval_required": "increase" in kind, "live_trading_enabled": False}


def build_risk_preset_proposal(kind: str, current: dict[str, float]) -> dict[str, object]:
    approval_required = "increase" in kind
    patch = dict(current)
    if kind.startswith("reduce"):
        patch = {key: value * 0.5 for key, value in current.items()}
    return {"status": "proposal", "kind": kind, "proposed_patch": patch, "mutates_active_profile": False, "approval_required": approval_required, "rollback_plan": "restore previous controlled profile", "live_trading_enabled": False}

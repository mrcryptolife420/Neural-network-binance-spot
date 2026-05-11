from __future__ import annotations

from typing import Any

from .portfolio_policy_registry import PortfolioPolicyRegistry


def rollback_to_previous_champion(registry: PortfolioPolicyRegistry, *, confirm: str) -> dict[str, Any]:
    current = registry.champion()
    if not current or not current.prev_champion_id:
        return {"status": "blocked", "reason": "previous_champion_missing", "live_trading_enabled": False}
    if confirm != "PAPER_POLICY_ROLLBACK":
        return {"status": "blocked", "reason": "confirmation_required", "live_trading_enabled": False}
    decision = registry.set_champion(current.prev_champion_id, operator_confirmed=True, evidence_refs=["rollback"])
    return {"status": "rolled_back", "decision": decision.__dict__, "live_trading_enabled": False}


def rollback_to_prev_champion(registry: PortfolioPolicyRegistry, *, confirm: str) -> dict[str, Any]:
    return rollback_to_previous_champion(registry, confirm=confirm)

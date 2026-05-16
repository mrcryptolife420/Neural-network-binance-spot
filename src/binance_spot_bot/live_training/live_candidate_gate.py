from __future__ import annotations

from typing import Any


def evaluate_live_candidate_gate(evidence: dict[str, Any], rehearsal: dict[str, Any]) -> dict[str, Any]:
    blockers = []
    if not evidence.get("manifest", {}).get("hashes"):
        blockers.append("evidence hashes required")
    if rehearsal.get("status") != "ok":
        blockers.append("more testnet evidence needed")
    blockers.append("live execution implementation gate required")
    return {"status": "blocked", "state": "live_execution_gate_required", "blockers": blockers, "live_execution_enabled": False, "live_trading_enabled": False}


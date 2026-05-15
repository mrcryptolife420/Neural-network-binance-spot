from __future__ import annotations

from typing import Any


SCENARIO_PROFILES = {
    "smoke_no_fill": {"steps": 3, "fills_expected": 0, "risk_blocks_expected": True},
    "smoke_with_fill": {"steps": 3, "fills_expected": 1, "risk_blocks_expected": False},
    "risk_block_expected": {"steps": 2, "fills_expected": 0, "risk_blocks_expected": True},
    "testnet_readiness_no_orders": {"steps": 1, "fills_expected": 0, "risk_blocks_expected": False},
}


def stabilize_paper_simulation(profile: str = "smoke_no_fill", result: dict[str, Any] | None = None) -> dict[str, Any]:
    scenario = SCENARIO_PROFILES.get(profile, SCENARIO_PROFILES["smoke_no_fill"])
    result = result or {"status": "ready", "fills": scenario["fills_expected"], "api_keys_required": False, "signed_endpoints_used": False}
    blockers = []
    if result.get("api_keys_required"):
        blockers.append("simulation must not require API keys")
    if result.get("signed_endpoints_used"):
        blockers.append("simulation must not use signed endpoints")
    if result.get("status") not in {"ok", "ready"}:
        blockers.append("simulation did not complete")
    status = "blocked" if blockers else "ok"
    return {
        "status": status,
        "profile": profile,
        "scenario": scenario,
        "blockers": blockers,
        "replay_artifact_required": bool(blockers),
        "live_trading_enabled": False,
    }


def paper_simulation_stabilizer(status: str) -> dict[str, Any]:
    return stabilize_paper_simulation(result={"status": status, "api_keys_required": False, "signed_endpoints_used": False})

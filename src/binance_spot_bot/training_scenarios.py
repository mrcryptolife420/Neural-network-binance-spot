from __future__ import annotations

from typing import Any


SCENARIOS = [
    ("scenario-001-first-health-check", "First health check", ["validate-config", "preflight"]),
    ("scenario-002-first-dashboard-launch", "First dashboard launch", ["dashboard-smoke"]),
    ("scenario-003-paper-session-smoke", "Paper session smoke", ["paper-os-simulation"]),
    ("scenario-012-no-live-proof-review", "No-live proof review", ["no-live-proof-pack"]),
]


def list_training_scenarios() -> dict[str, Any]:
    scenarios = [
        {
            "scenario_id": scenario_id,
            "title": title,
            "difficulty": "beginner",
            "commands": commands,
            "pass_criteria": ["command exits successfully", "live_trading_enabled is false"],
            "no_live_proof": True,
            "live_trading_enabled": False,
        }
        for scenario_id, title, commands in SCENARIOS
    ]
    return {"status": "ok", "scenarios": scenarios, "live_trading_enabled": False}


def run_training_scenario(scenario_id: str) -> dict[str, Any]:
    scenarios = {row["scenario_id"]: row for row in list_training_scenarios()["scenarios"]}
    if scenario_id not in scenarios:
        return {"status": "blocked", "reason": "unknown scenario", "live_trading_enabled": False}
    return {"status": "ready", "scenario": scenarios[scenario_id], "execute_commands": False, "live_trading_enabled": False}


def training_scenarios() -> dict[str, Any]:
    return list_training_scenarios()

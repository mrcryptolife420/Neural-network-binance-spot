from __future__ import annotations

from typing import Any

from .regression_risk import score_regression_risk
from .test_impact_map import select_tests_for_changes
from .test_profiles import PROFILE_COMMANDS, validate_profile_for_risk


def select_intelligent_tests(changed: list[str], policy: str = "balanced") -> dict[str, Any]:
    risk = score_regression_risk(changed)
    profile = risk["payload"]["profile"]
    if policy == "strict":
        profile = "deep"
    elif policy == "fast" and validate_profile_for_risk("fast", risk["payload"]["level"])["status"] == "ok":
        profile = "fast"
    impact = select_tests_for_changes(changed, strict=profile == "deep")
    commands = list(dict.fromkeys(impact["payload"]["tests"] + PROFILE_COMMANDS.get(profile, [])))
    blockers = []
    if policy == "fast" and risk["payload"]["level"] in {"high", "critical"}:
        blockers.append("fast_profile_blocked_for_safety_critical_change")
    return {
        "status": "blocked" if blockers else "ready",
        "selected_profile": profile,
        "selected_commands": commands,
        "skipped_commands": [],
        "estimated_runtime_ms": len(commands) * 30000,
        "risk": risk["payload"],
        "blockers": blockers,
        "explanation": impact["payload"]["reasons"],
        "live_trading_enabled": False,
    }


def selected_tests(changed: list[str]) -> dict[str, Any]:
    payload = select_intelligent_tests(changed)
    payload["payload"] = {"tests": payload["selected_commands"], "profile": payload["selected_profile"], "risk": payload["risk"]}
    return payload

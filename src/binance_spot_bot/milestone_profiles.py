from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class MilestoneProfile:
    name: str
    commands: list[str]
    required_evidence: list[str]
    confirm_phrase: str = ""
    browser_smoke_required: bool = False
    safe_env: dict[str, str] = field(
        default_factory=lambda: {"PYTHONPATH": "src", "LIVE_TRADING_ENABLED": "false", "KILL_SWITCH": "true"}
    )
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_milestone_profiles() -> dict[str, MilestoneProfile]:
    fast = MilestoneProfile(
        name="fast_milestone",
        commands=["system-inventory", "system-safety-invariants", "operator-quality-gate", "evidence-manifest"],
        required_evidence=["system_inventory", "safety_invariants", "operator_quality_gate"],
    )
    standard = MilestoneProfile(
        name="standard_milestone",
        commands=fast.commands + ["dashboard-smoke", "roadmap-traceability-audit", "paper-os-simulation"],
        required_evidence=fast.required_evidence + ["dashboard_smoke", "roadmap_traceability", "paper_simulation"],
        confirm_phrase="RUN_STANDARD_MILESTONE",
    )
    deep = MilestoneProfile(
        name="deep_milestone",
        commands=standard.commands + ["no-live-proof-pack", "production-readiness-simulation", "milestone-evidence-graph"],
        required_evidence=standard.required_evidence + ["no_live_proof", "readiness_simulation", "evidence_graph"],
        confirm_phrase="RUN_DEEP_MILESTONE",
        browser_smoke_required=True,
    )
    release = MilestoneProfile(
        name="release_candidate_milestone",
        commands=deep.commands + ["system-audit-report", "milestone-bundle-export", "milestone-bundle-verify"],
        required_evidence=deep.required_evidence + ["system_audit_report", "milestone_bundle", "bundle_verification"],
        confirm_phrase="RUN_RELEASE_CANDIDATE_MILESTONE",
        browser_smoke_required=True,
    )
    return {profile.name: profile for profile in (fast, standard, deep, release)}


def get_milestone_profile(name: str) -> MilestoneProfile:
    profiles = build_milestone_profiles()
    if name not in profiles:
        raise KeyError(f"unknown milestone profile: {name}")
    return profiles[name]


def milestone_profiles() -> dict[str, Any]:
    profiles = build_milestone_profiles()
    return {
        "status": "ready",
        "profiles": {name: profile.to_dict() for name, profile in profiles.items()},
        "live_trading_enabled": False,
    }

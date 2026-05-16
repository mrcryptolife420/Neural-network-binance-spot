from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import has_advice_wording, json_write, redact_value, to_plain

from . import FORBIDDEN_RUNTIME_ACTIONS, NO_LIVE_AUTO_START_STATEMENT, SAFE_ENV_DEFAULTS, SECRET_FREE_PACKAGE_STATEMENT

ALLOWED_EXTRAS = {"ui", "visual", "research", "realtime", "mlops", "dev"}


@dataclass
class PackageDependencyGroup:
    name: str
    extras: list[str]


@dataclass
class PackageProfile:
    profile_id: str
    name: str
    description: str
    extras: list[str] = field(default_factory=list)
    include_dashboard: bool = True
    include_research: bool = False
    include_visual_smoke: bool = False
    include_live_ops: bool = False
    include_dev_tools: bool = False
    safe_env_defaults: dict[str, str] = field(default_factory=lambda: dict(SAFE_ENV_DEFAULTS))
    forbidden_runtime_actions: list[str] = field(default_factory=lambda: list(FORBIDDEN_RUNTIME_ACTIONS))
    no_live_auto_start_statement: str = NO_LIVE_AUTO_START_STATEMENT
    secret_free_package_statement: str = SECRET_FREE_PACKAGE_STATEMENT


@dataclass
class PackageProfileValidationResult:
    profile_id: str
    status: str
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class PackageProfileReport:
    status: str
    profiles: list[PackageProfile]
    validations: list[PackageProfileValidationResult]
    no_live_auto_start_statement: str = NO_LIVE_AUTO_START_STATEMENT
    secret_free_package_statement: str = SECRET_FREE_PACKAGE_STATEMENT


def default_package_profiles() -> list[PackageProfile]:
    return [
        PackageProfile("minimal-operator", "Minimal Operator", "CLI and Control Center", []),
        PackageProfile("dashboard-full", "Dashboard Full", "Dashboard V2 local app", ["ui", "visual"], include_visual_smoke=True),
        PackageProfile("research-local", "Research Local", "Local research and dataset tooling", ["research", "mlops"], include_research=True),
        PackageProfile("live-ops-safe", "Live Ops Safe", "Dashboard plus governance/live-ops safety", ["ui"], include_live_ops=True),
        PackageProfile("developer", "Developer", "All local development tooling", ["ui", "visual", "research", "realtime", "mlops", "dev"], include_research=True, include_visual_smoke=True, include_live_ops=True, include_dev_tools=True),
    ]


def validate_package_profile(profile: PackageProfile) -> PackageProfileValidationResult:
    blockers: list[str] = []
    unknown = [extra for extra in profile.extras if extra not in ALLOWED_EXTRAS]
    if unknown:
        blockers.append(f"unknown extras: {','.join(unknown)}")
    if profile.safe_env_defaults.get("LIVE_TRADING_ENABLED") != "false":
        blockers.append("LIVE_TRADING_ENABLED must default to false")
    if profile.safe_env_defaults.get("KILL_SWITCH") != "true":
        blockers.append("KILL_SWITCH must default to true")
    if not profile.forbidden_runtime_actions:
        blockers.append("forbidden runtime actions missing")
    for action in ("place_order", "start_live_session", "arm_live"):
        if action not in profile.forbidden_runtime_actions:
            blockers.append(f"forbidden action missing: {action}")
    if profile.no_live_auto_start_statement != NO_LIVE_AUTO_START_STATEMENT:
        blockers.append("no live auto-start statement missing")
    if has_advice_wording(profile):
        blockers.append("advice wording blocked")
    return PackageProfileValidationResult(profile.profile_id, "blocked" if blockers else "ok", blockers)


def package_profile_report_to_dict(report: PackageProfileReport) -> dict[str, Any]:
    payload = redact_value(to_plain(report))
    payload["live_trading_enabled"] = False
    payload["live_order_submitted"] = False
    return payload


def build_package_profile_report() -> dict[str, Any]:
    profiles = default_package_profiles()
    validations = [validate_package_profile(profile) for profile in profiles]
    status = "ok" if all(item.status == "ok" for item in validations) else "blocked"
    return package_profile_report_to_dict(PackageProfileReport(status, profiles, validations))


def write_package_profile_report(root: Path) -> dict[str, Any]:
    return json_write(root / "dist" / "package-reports" / "package_profiles.json", build_package_profile_report())

from __future__ import annotations

import importlib.util
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .config import BotSettings
from .credentials import CredentialManager
from .security import scan_for_secrets


@dataclass(frozen=True)
class PreflightCheck:
    name: str
    status: str
    message: str
    blocking: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PreflightReport:
    status: str
    checks: list[PreflightCheck]

    def to_dict(self) -> dict[str, Any]:
        return {"status": self.status, "checks": [check.to_dict() for check in self.checks]}


def run_preflight(settings: BotSettings, root: Path | None = None, include_security_scan: bool = True) -> PreflightReport:
    root = root or Path.cwd()
    checks = [
        _config_check(settings),
        _live_disabled_check(settings),
        _data_dirs_check(settings),
        _dependency_check("streamlit"),
        _credential_check(settings),
    ]
    if include_security_scan:
        checks.append(_secret_scan_check(root))
    status = "blocked" if any(check.blocking and check.status != "ok" for check in checks) else "ok"
    return PreflightReport(status, checks)


def _config_check(settings: BotSettings) -> PreflightCheck:
    try:
        settings.validate_startup()
    except Exception as exc:
        return PreflightCheck("config", "blocked", str(exc), True)
    return PreflightCheck("config", "ok", "configuration validates")


def _live_disabled_check(settings: BotSettings) -> PreflightCheck:
    if settings.live_trading_enabled:
        return PreflightCheck("live_disabled", "blocked", "LIVE_TRADING_ENABLED must stay false", True)
    return PreflightCheck("live_disabled", "ok", "live trading disabled")


def _data_dirs_check(settings: BotSettings) -> PreflightCheck:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    return PreflightCheck("data_dirs", "ok", f"data dir ready: {settings.data_dir}")


def _dependency_check(module: str) -> PreflightCheck:
    if importlib.util.find_spec(module) is None:
        return PreflightCheck(f"dependency_{module}", "warning", f"{module} is not installed")
    return PreflightCheck(f"dependency_{module}", "ok", f"{module} available")


def _credential_check(settings: BotSettings) -> PreflightCheck:
    manager = CredentialManager()
    status = manager.status().to_dict()
    if settings.exchange_profile == "local-demo":
        return PreflightCheck("credentials", "ok", "local demo does not require credentials")
    if not status.get("has_api_key") or not status.get("has_api_secret"):
        return PreflightCheck("credentials", "warning", "credentials not loaded for selected exchange profile")
    return PreflightCheck("credentials", "ok", "credentials loaded in session")


def _secret_scan_check(root: Path) -> PreflightCheck:
    findings = scan_for_secrets(root)
    if findings:
        return PreflightCheck("secret_scan", "blocked", f"{len(findings)} possible secret artifacts found", True)
    return PreflightCheck("secret_scan", "ok", "no secret artifacts found")

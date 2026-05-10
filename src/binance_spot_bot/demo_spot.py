from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any

from .exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from .redaction import redact_payload

DEMO_SPOT_BASE_URL = "https://demo-api.binance.com"


@dataclass(frozen=True)
class DemoSpotConnectionState:
    profile: str
    base_url: str
    connected: bool
    authenticated: bool
    server_time_ok: bool
    account_ok: bool
    trading_permission_ok: bool
    armed: bool
    kill_switch: bool
    last_error: str = ""
    api_key_fingerprint: str = "not-configured"
    checked_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class DemoTradingGateResult:
    allowed: bool
    reason: str
    checks: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def connection_state_from_report(
    report: dict[str, Any],
    *,
    armed: bool = False,
    kill_switch: bool = True,
    api_key_fingerprint: str = "not-configured",
) -> DemoSpotConnectionState:
    checks = {item.get("name"): item for item in report.get("checks", [])}
    signed = checks.get("signed_account", {})
    account_ok = signed.get("status") == "ok"
    return DemoSpotConnectionState(
        profile=str(report.get("profile", {}).get("name", "")),
        base_url=str(report.get("base_url", "")),
        connected=report.get("status") == "ok",
        authenticated=account_ok,
        server_time_ok=checks.get("server_time", {}).get("status") == "ok",
        account_ok=account_ok,
        trading_permission_ok=bool(signed.get("details", {}).get("canTrade", False)),
        armed=armed,
        kill_switch=kill_switch,
        last_error=_first_error(report),
        api_key_fingerprint=api_key_fingerprint,
        checked_at_ms=int(report.get("checked_at_ms") or time.time() * 1000),
    )


def evaluate_demo_trading_gate(
    *,
    profile: str,
    base_url: str,
    has_credentials: bool,
    connection_ok: bool,
    armed: bool,
    live_trading_enabled: bool,
    kill_switch: bool,
    risk_allowed: bool,
    filters_loaded: bool,
    max_orders_ok: bool,
) -> DemoTradingGateResult:
    checks = {
        "profile_is_demo_spot": profile == BINANCE_DEMO_SPOT_PROFILE,
        "base_url_is_demo": normalize_base_url(base_url) == DEMO_SPOT_BASE_URL,
        "credentials_present": has_credentials,
        "connection_ok": connection_ok,
        "armed": armed,
        "live_disabled": not live_trading_enabled,
        "kill_switch_off": not kill_switch,
        "risk_allowed": risk_allowed,
        "filters_loaded": filters_loaded,
        "max_orders_ok": max_orders_ok,
    }
    failed = [name for name, ok in checks.items() if not ok]
    return DemoTradingGateResult(not failed, "allowed" if not failed else ", ".join(failed), checks)


def normalize_base_url(base_url: str) -> str:
    value = base_url.rstrip("/")
    if value.endswith("/api"):
        value = value[:-4]
    return value


def _first_error(report: dict[str, Any]) -> str:
    for item in report.get("checks", []):
        if item.get("status") not in {"ok", "ready"}:
            return str(item.get("message", ""))
    return ""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Any

from binance_spot_bot.redaction import redact_payload

SUPPORTED_MODES = ("demo", "paper", "testnet-readiness")
SUPPORTED_SOURCES = ("auto", "demo", "rest", "websocket")


def dashboard_v2_no_live_statement() -> str:
    return "LOCAL REALTIME DASHBOARD - NO LIVE TRADING"


def _json_safe(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {key: _json_safe(val) for key, val in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value


def redact_dashboard_payload(payload: Any) -> Any:
    return redact_payload(_json_safe(payload))


@dataclass(frozen=True)
class DashboardV2Health:
    status: str = "ok"
    app_name: str = "Dashboard V2"
    version: str = "0.1.0"
    supported_modes: tuple[str, ...] = SUPPORTED_MODES
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


@dataclass(frozen=True)
class DashboardV2Config:
    supported_modes: tuple[str, ...] = SUPPORTED_MODES
    supported_sources: tuple[str, ...] = SUPPORTED_SOURCES
    default_symbol: str = "BTCUSDT"
    default_interval: str = "1m"
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


@dataclass(frozen=True)
class DashboardV2Page:
    key: str
    title: str
    route: str
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


@dataclass(frozen=True)
class DashboardV2RuntimeSnapshot:
    status: str
    mode: str
    symbol: str
    candles: list[dict[str, Any]] = field(default_factory=list)
    signals: list[dict[str, Any]] = field(default_factory=list)
    fills: list[dict[str, Any]] = field(default_factory=list)
    equity: list[dict[str, Any]] = field(default_factory=list)
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False

    def to_dict(self, *, limit: int = 250) -> dict[str, Any]:
        payload = asdict(self)
        for key in ("candles", "signals", "fills", "equity"):
            payload[key] = payload[key][-limit:]
        return redact_dashboard_payload(payload)


@dataclass(frozen=True)
class DashboardV2ActionRequest:
    action: str
    mode: str = "demo"
    confirm: str = ""
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DashboardV2ActionResult:
    status: str
    action: str
    reason: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


@dataclass(frozen=True)
class DashboardV2Event:
    topic: str
    payload: dict[str, Any]
    ts_ms: int
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


@dataclass(frozen=True)
class DashboardV2Error:
    status: str = "error"
    message: str = ""
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))

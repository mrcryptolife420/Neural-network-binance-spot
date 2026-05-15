from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .redaction import redact_payload


@dataclass
class RuntimeIdentity:
    mode: str = "demo"
    symbol: str = "BTCUSDT"
    interval: str = "1m"
    session_id: str = ""


@dataclass
class RuntimeLifecycleState:
    status: str = "ready"
    message: str = ""
    resume_required: bool = False


@dataclass
class RuntimeMarketState:
    candle: dict[str, Any] = field(default_factory=dict)
    candles: list[dict[str, Any]] = field(default_factory=list)
    top_of_book: dict[str, Any] = field(default_factory=dict)
    data_quality: dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimePaperState:
    balances: dict[str, Any] = field(default_factory=dict)
    fills: list[dict[str, Any]] = field(default_factory=list)
    equity_points: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RuntimeModelState:
    latest_signal: dict[str, Any] = field(default_factory=dict)
    latest_risk_decision: dict[str, Any] = field(default_factory=dict)
    signal_points: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RuntimeDemoState:
    demo_pilot_counters: dict[str, Any] = field(default_factory=dict)
    reconciliation: dict[str, Any] = field(default_factory=dict)
    order_lifecycle: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RuntimeReportState:
    report_paths: dict[str, str] = field(default_factory=dict)
    alerts_summary: dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimeSafetyState:
    live_trading_enabled: bool = False
    kill_switch: bool = True
    credential_fingerprint: str = ""


@dataclass
class RuntimeState:
    identity: RuntimeIdentity = field(default_factory=RuntimeIdentity)
    lifecycle: RuntimeLifecycleState = field(default_factory=RuntimeLifecycleState)
    market: RuntimeMarketState = field(default_factory=RuntimeMarketState)
    paper: RuntimePaperState = field(default_factory=RuntimePaperState)
    model: RuntimeModelState = field(default_factory=RuntimeModelState)
    demo: RuntimeDemoState = field(default_factory=RuntimeDemoState)
    reports: RuntimeReportState = field(default_factory=RuntimeReportState)
    safety: RuntimeSafetyState = field(default_factory=RuntimeSafetyState)

    def to_dict(self) -> dict[str, Any]:
        payload = redact_payload(asdict(self))
        payload["live_trading_enabled"] = False
        return payload

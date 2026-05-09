from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class WatchdogAction(str, Enum):
    OBSERVE = "observe"
    BLOCK_TRADING = "block_trading"
    PAUSE_RUNTIME = "pause_runtime"
    STOP_RUNTIME = "stop_runtime"


@dataclass(frozen=True)
class Alert:
    name: str
    severity: AlertSeverity
    message: str
    action: WatchdogAction
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["severity"] = self.severity.value
        payload["action"] = self.action.value
        return payload


class AlertManager:
    def __init__(self) -> None:
        self._alerts: list[Alert] = []

    def emit(
        self,
        name: str,
        severity: AlertSeverity,
        message: str,
        action: WatchdogAction | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Alert:
        alert = Alert(name, severity, message, action or default_action_for(severity), metadata=metadata or {})
        self._alerts.append(alert)
        return alert

    def alerts(self) -> list[Alert]:
        return list(self._alerts)

    def should_block_trading(self) -> bool:
        return any(alert.action in {WatchdogAction.BLOCK_TRADING, WatchdogAction.PAUSE_RUNTIME, WatchdogAction.STOP_RUNTIME} for alert in self._alerts)

    def should_stop_runtime(self) -> bool:
        return any(alert.action == WatchdogAction.STOP_RUNTIME for alert in self._alerts)

    def to_dict(self) -> dict[str, Any]:
        return {"alerts": [alert.to_dict() for alert in self._alerts]}


def default_action_for(severity: AlertSeverity) -> WatchdogAction:
    if severity == AlertSeverity.CRITICAL:
        return WatchdogAction.STOP_RUNTIME
    if severity == AlertSeverity.ERROR:
        return WatchdogAction.BLOCK_TRADING
    return WatchdogAction.OBSERVE

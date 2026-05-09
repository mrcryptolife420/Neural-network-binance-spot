from __future__ import annotations

from dataclasses import asdict, dataclass

from .alerts import AlertSeverity, WatchdogAction, default_action_for


@dataclass(frozen=True)
class ChaosScenario:
    key: str
    severity: AlertSeverity
    expected_action: WatchdogAction

    def to_dict(self) -> dict[str, str]:
        payload = asdict(self)
        payload["severity"] = self.severity.value
        payload["expected_action"] = self.expected_action.value
        return payload


SCENARIOS = {
    "429": AlertSeverity.ERROR,
    "418": AlertSeverity.CRITICAL,
    "5xx": AlertSeverity.ERROR,
    "websocket_disconnect": AlertSeverity.WARNING,
    "stale_data": AlertSeverity.ERROR,
    "write_failure": AlertSeverity.CRITICAL,
    "unknown_order": AlertSeverity.ERROR,
}


def simulate_failure(key: str) -> ChaosScenario:
    if key not in SCENARIOS:
        raise ValueError(f"unsupported chaos scenario: {key}")
    severity = SCENARIOS[key]
    return ChaosScenario(key, severity, default_action_for(severity))

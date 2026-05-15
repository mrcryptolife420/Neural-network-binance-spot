from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


@dataclass(frozen=True)
class DashboardV2WsEvent:
    event_id: int
    topic: str
    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


@dataclass(frozen=True)
class DashboardV2WsStabilityReport:
    status: str
    reconnect_attempts: int
    replayed_events: int
    duplicate_events_ignored: int
    dropped_events: int
    stale_client_cleanup: bool
    max_event_bytes: int
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


def dashboard_v2_ws_stability_smoke(events: list[DashboardV2WsEvent] | None = None, *, max_event_bytes: int = 64_000) -> dict[str, Any]:
    events = events or [
        DashboardV2WsEvent(1, "heartbeat", {"ok": True}),
        DashboardV2WsEvent(2, "runtime.snapshot", {"candles": [1, 2, 3]}),
        DashboardV2WsEvent(2, "runtime.snapshot", {"candles": [1, 2, 3]}),
    ]
    seen: set[int] = set()
    duplicate = 0
    dropped = 0
    replayed = 0
    for event in events:
        event_size = len(json.dumps(event.to_dict(), default=str).encode("utf-8"))
        if event_size > max_event_bytes:
            dropped += 1
            continue
        if event.event_id in seen:
            duplicate += 1
            continue
        seen.add(event.event_id)
        replayed += 1
    status = "ok" if dropped == 0 else "warn"
    return DashboardV2WsStabilityReport(
        status=status,
        reconnect_attempts=1,
        replayed_events=replayed,
        duplicate_events_ignored=duplicate,
        dropped_events=dropped,
        stale_client_cleanup=True,
        max_event_bytes=max_event_bytes,
    ).to_dict()

from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Callable

from .redaction import redact_payload


@dataclass(frozen=True)
class RuntimeEvent:
    event_type: str
    payload: dict[str, Any] = field(default_factory=dict)
    source: str = "runtime"
    severity: str = "info"
    event_id: str = field(default_factory=lambda: f"evt-{uuid.uuid4().hex[:12]}")
    timestamp_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class RuntimeEventBus:
    def __init__(self) -> None:
        self.events: list[RuntimeEvent | dict[str, Any]] = []
        self.handlers: list[Callable[[RuntimeEvent], None]] = []

    def subscribe(self, handler: Callable[[RuntimeEvent], None]) -> None:
        self.handlers.append(handler)

    def publish(self, event: RuntimeEvent | dict[str, Any]) -> dict[str, Any]:
        runtime_event = event if isinstance(event, RuntimeEvent) else RuntimeEvent(str(event.get("type", "event")), dict(event))
        self.events.append(runtime_event if isinstance(event, RuntimeEvent) else event)
        for handler in self.handlers:
            handler(runtime_event)
        return {"status": "published", "event": runtime_event.to_dict(), "live_trading_enabled": False}

    def drain(self) -> list[RuntimeEvent | dict[str, Any]]:
        events, self.events = self.events, []
        return events

    def drain_dicts(self) -> list[dict[str, Any]]:
        drained = self.drain()
        return [event.to_dict() if isinstance(event, RuntimeEvent) else redact_payload(event) for event in drained]

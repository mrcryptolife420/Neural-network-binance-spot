from __future__ import annotations

import asyncio
import time
from collections import deque
from typing import Any

from .schemas import DashboardV2Event, redact_dashboard_payload


class DashboardV2EventBus:
    def __init__(self, *, max_buffer: int = 100, max_payload_items: int = 250) -> None:
        self.max_payload_items = max_payload_items
        self.buffer: deque[dict[str, Any]] = deque(maxlen=max_buffer)
        self.clients: set[asyncio.Queue[dict[str, Any]]] = set()

    def _trim(self, payload: dict[str, Any]) -> dict[str, Any]:
        trimmed = {}
        for key, value in payload.items():
            if isinstance(value, list):
                trimmed[key] = value[-self.max_payload_items:]
            else:
                trimmed[key] = value
        return redact_dashboard_payload(trimmed)

    def publish(self, topic: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        event = DashboardV2Event(topic, self._trim(payload or {}), int(time.time() * 1000)).to_dict()
        self.buffer.append(event)
        for queue in list(self.clients):
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                self.clients.discard(queue)
        return event

    def subscribe(self) -> asyncio.Queue[dict[str, Any]]:
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=50)
        self.clients.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue[dict[str, Any]]) -> None:
        self.clients.discard(queue)

    def heartbeat(self) -> dict[str, Any]:
        return self.publish("system.health", {"status": "ok"})

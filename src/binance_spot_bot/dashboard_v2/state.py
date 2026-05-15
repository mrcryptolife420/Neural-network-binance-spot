from __future__ import annotations

import threading
import time
from typing import Any

from .event_bus import DashboardV2EventBus
from .runtime_bridge import DashboardRuntimeBridge


class DashboardV2Loop:
    def __init__(self, bridge: DashboardRuntimeBridge, bus: DashboardV2EventBus, *, tick_seconds: float = 1.0) -> None:
        self.bridge = bridge
        self.bus = bus
        self.tick_seconds = tick_seconds
        self.state = "idle"
        self.errors = 0
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> dict[str, Any]:
        if self._thread and self._thread.is_alive():
            return {"status": "ok", "loop_state": self.state, "live_trading_enabled": False}
        self._stop.clear()
        self.state = "running"
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return {"status": "ok", "loop_state": self.state, "live_trading_enabled": False}

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                self.bridge.step()
                self.bus.publish("runtime.snapshot", self.bridge.snapshot())
            except Exception as exc:
                self.errors += 1
                self.bus.publish("dashboard.error", {"error": str(exc)})
            time.sleep(self.tick_seconds)
        self.state = "stopped"

    def stop(self) -> dict[str, Any]:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2.0)
        self.bridge.stop()
        return {"status": "ok", "loop_state": self.state, "live_trading_enabled": False}

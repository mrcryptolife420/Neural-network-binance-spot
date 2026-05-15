from __future__ import annotations

from typing import Any


class RuntimeDemoPilotService:
    def __init__(self) -> None:
        self.counters = {"starts": 0, "stops": 0, "reconciliations": 0}

    def record_start(self) -> dict[str, Any]:
        self.counters["starts"] += 1
        return self.status()

    def record_stop(self) -> dict[str, Any]:
        self.counters["stops"] += 1
        return self.status()

    def record_reconciliation(self) -> dict[str, Any]:
        self.counters["reconciliations"] += 1
        return self.status()

    def status(self) -> dict[str, Any]:
        return {"status": "ready", "counters": dict(self.counters), "live_trading_enabled": False}

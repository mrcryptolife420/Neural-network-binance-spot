from __future__ import annotations

import threading
from dataclasses import asdict, dataclass, field
from typing import Any

from .schemas import DashboardV2RuntimeSnapshot, SUPPORTED_MODES, redact_dashboard_payload


@dataclass
class DashboardRuntimeConfig:
    mode: str = "demo"
    source: str = "demo"
    symbol: str = "BTCUSDT"
    interval: str = "1m"
    scenario: str = "sideways"
    model_alias: str = "demo"


@dataclass
class DashboardRuntimeBridgeState:
    status: str = "idle"
    config: DashboardRuntimeConfig = field(default_factory=DashboardRuntimeConfig)
    steps: int = 0
    live_trading_enabled: bool = False


class DashboardRuntimeBridge:
    def __init__(self, runtime: Any | None = None) -> None:
        self.runtime = runtime
        self.state = DashboardRuntimeBridgeState()
        self._lock = threading.RLock()

    def configure(self, config: DashboardRuntimeConfig) -> dict[str, Any]:
        if config.mode not in SUPPORTED_MODES:
            return {"status": "blocked", "reason": "live/unsupported mode blocked", "live_trading_enabled": False}
        with self._lock:
            self.state.config = config
        return {"status": "ok", "config": asdict(config), "live_trading_enabled": False}

    def start(self) -> dict[str, Any]:
        with self._lock:
            if self.state.config.mode not in SUPPORTED_MODES:
                return {"status": "blocked", "reason": "unsupported mode", "live_trading_enabled": False}
            self.state.status = "running"
        return {"status": "ok", "runtime_status": "running", "live_trading_enabled": False}

    def stop(self) -> dict[str, Any]:
        with self._lock:
            self.state.status = "stopped"
        return {"status": "ok", "runtime_status": "stopped", "live_trading_enabled": False}

    def step(self) -> dict[str, Any]:
        with self._lock:
            self.state.steps += 1
        return {"status": "ok", "steps": self.state.steps, "live_trading_enabled": False}

    def snapshot(self) -> dict[str, Any]:
        cfg = self.state.config
        snap = DashboardV2RuntimeSnapshot(self.state.status, cfg.mode, cfg.symbol, candles=[{"close": "100", "t": self.state.steps}])
        return redact_dashboard_payload(snap.to_dict() | {"source": cfg.source, "interval": cfg.interval, "steps": self.state.steps})

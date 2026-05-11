from __future__ import annotations

import time
from contextlib import contextmanager

from .dev_quality_facade import profile_payload


def dashboard_profile(elapsed_ms: float):
    return profile_payload("dashboard", elapsed_ms)


class DashboardProfiler:
    def __init__(self):
        self.samples = []

    @contextmanager
    def measure(self, name: str):
        started = time.perf_counter()
        try:
            yield
        finally:
            self.samples.append({"name": name, "elapsed_ms": round((time.perf_counter() - started) * 1000, 6)})

    def to_dict(self):
        return {"samples": self.samples, "live_trading_enabled": False}

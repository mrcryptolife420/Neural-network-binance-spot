from __future__ import annotations

import contextlib
from typing import Any, Iterator

from .profiling_core import ProfileRun, profile_block, summarize_profile_run


class DashboardProfiler:
    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled
        self.run = ProfileRun("dashboard-profile", "dashboard")

    @contextlib.contextmanager
    def measure(self, name: str, labels: dict[str, Any] | None = None) -> Iterator[None]:
        if not self.enabled:
            yield
            return
        with profile_block(name, "dashboard", labels or {}, self.run):
            yield

    def summary(self) -> dict[str, Any]:
        return summarize_profile_run(self.run)

    def to_dict(self) -> dict[str, Any]:
        run = self.run.to_dict()
        return {
            "status": "ready",
            "run": run,
            "samples": run["spans"],
            "summary": self.summary(),
            "live_trading_enabled": False,
        }


def profile_dashboard_panels(panels: list[str]) -> dict[str, Any]:
    profiler = DashboardProfiler()
    for panel in panels:
        with profiler.measure(panel, {"panel": panel}):
            pass
    payload = profiler.to_dict()
    payload["slow_panels"] = [span for span in payload["run"]["spans"] if span["duration_ms"] > 500]
    return payload


def dashboard_profile(elapsed_ms: float) -> dict[str, Any]:
    return {"status": "ok" if elapsed_ms <= 1000 else "warn", "payload": {"elapsed_ms": elapsed_ms}, "live_trading_enabled": False}

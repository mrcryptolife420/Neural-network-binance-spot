from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from .runtime_event_bus import RuntimeEvent, RuntimeEventBus


@dataclass(frozen=True)
class RuntimeStageResult:
    name: str
    status: str
    duration_ms: float
    payload: dict[str, Any] = field(default_factory=dict)
    live_trading_enabled: bool = False


class RuntimeStepPipeline:
    def __init__(self, stages: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]], event_bus: RuntimeEventBus | None = None) -> None:
        self.stages = stages
        self.event_bus = event_bus or RuntimeEventBus()

    def run(self, context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = dict(context or {})
        results: list[RuntimeStageResult] = []
        for name, stage in self.stages:
            started = time.perf_counter()
            try:
                ctx.update(stage(ctx))
                status = "ok"
            except Exception as exc:
                ctx["error"] = exc.__class__.__name__
                status = "failed"
            duration = (time.perf_counter() - started) * 1000
            result = RuntimeStageResult(name, status, duration, {"keys": sorted(ctx.keys())})
            results.append(result)
            self.event_bus.publish(RuntimeEvent("runtime.stage", {"stage": name, "status": status, "duration_ms": duration}))
            if status != "ok":
                break
        return {"status": "ok" if all(row.status == "ok" for row in results) else "failed", "stages": [row.__dict__ for row in results], "context": ctx, "live_trading_enabled": False}

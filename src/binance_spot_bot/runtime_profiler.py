from __future__ import annotations

from typing import Any, Callable

from .profiling_core import ProfileRun, profile_block, summarize_profile_run


RUNTIME_STEPS = ["start", "data_source.next_event", "data_quality", "feature_row", "model_signal", "risk_decision", "paper_execution", "snapshot"]


def profile_runtime_steps(step_runner: Callable[[str], Any] | None = None, steps: list[str] | None = None) -> dict[str, Any]:
    run = ProfileRun("runtime-profile", "runtime")
    for step in steps or RUNTIME_STEPS:
        with profile_block(step, "runtime", {"step": step}, run):
            if step_runner:
                step_runner(step)
    return {"status": "ready", "run": run.to_dict(), "summary": summarize_profile_run(run), "live_trading_enabled": False}


def runtime_profile(elapsed_ms: float) -> dict[str, Any]:
    return {"status": "ok" if elapsed_ms <= 1000 else "warn", "payload": {"elapsed_ms": elapsed_ms}, "live_trading_enabled": False}

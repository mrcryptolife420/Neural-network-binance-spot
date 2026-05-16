from __future__ import annotations

from typing import Any


def simulate_rebalance_events(allocation: dict[str, Any], schedule: dict[str, Any], *, steps: int = 48) -> dict[str, Any]:
    interval = int(schedule.get("interval_steps", 12))
    max_rebalances = int(schedule.get("max_rebalances", 6))
    events = []
    skipped = []
    last_step = -999
    for step in range(interval, steps + 1, interval):
        if len(events) >= max_rebalances:
            skipped.append({"step": step, "reason": "max_rebalances_reached"})
            continue
        if step - last_step < int(schedule.get("min_steps_between_rebalances", 1)):
            skipped.append({"step": step, "reason": "min_steps_between_rebalances"})
            continue
        events.append(
            {
                "event_id": f"rebalance-{schedule.get('schedule_id', 'schedule')}-{step}",
                "step": step,
                "event_type": schedule.get("schedule_type", "fixed_interval"),
                "estimated_turnover": round(len(allocation.get("items", [])) * 0.01, 6),
                "estimated_fees": round(len(allocation.get("items", [])) * 0.25, 6),
                "paper_only": True,
                "live_trading_enabled": False,
            }
        )
        last_step = step
    return {"status": "ok", "events": events, "skipped": skipped, "live_trading_enabled": False}


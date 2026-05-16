from __future__ import annotations

from typing import Any


def evaluate_demo_dataset_quality(recording: dict[str, Any] | None = None, *, required_sessions: int = 1, required_fills: int = 1) -> dict[str, Any]:
    events = (recording or {}).get("manifest", {}).get("events", [])
    fills = [event for event in events if "fill" in str(event.get("type", ""))]
    blockers = []
    if required_sessions > 1:
        blockers.append("minimum demo sessions not met")
    if len(fills) < required_fills:
        blockers.append("minimum demo fills not met")
    if any("live" in str(event.get("type", "")).lower() for event in events):
        blockers.append("live events mixed into demo dataset")
    score = max(0.0, 100.0 - len(blockers) * 35.0)
    return {"status": "blocked" if blockers else "ok", "quality_score": score, "blockers": blockers, "warnings": [], "fills": len(fills), "live_trading_enabled": False}


from __future__ import annotations

from typing import Any


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def feature_drift(current: list[float], baseline: list[float], threshold: float = 0.2) -> dict[str, Any]:
    score = abs(_mean(current) - _mean(baseline))
    status = "warn" if score > threshold else "ok"
    return {
        "status": status,
        "payload": {
            "status": status,
            "score": round(score, 6),
            "threshold": threshold,
            "current_mean": round(_mean(current), 6),
            "baseline_mean": round(_mean(baseline), 6),
        },
        "live_trading_enabled": False,
    }

from __future__ import annotations

from typing import Any


def model_health_score(drift: float, performance_ok: bool, *, latency_ok: bool = True, calibration_ok: bool = True) -> dict[str, Any]:
    penalty = int(max(0.0, drift) * 100)
    if not performance_ok:
        penalty += 25
    if not latency_ok:
        penalty += 10
    if not calibration_ok:
        penalty += 10
    score = max(0, 100 - penalty)
    status = "ok" if score >= 80 else "warn" if score >= 50 else "blocked"
    return {"status": status, "score": score, "components": {"drift": drift, "performance_ok": performance_ok, "latency_ok": latency_ok, "calibration_ok": calibration_ok}, "live_trading_enabled": False}

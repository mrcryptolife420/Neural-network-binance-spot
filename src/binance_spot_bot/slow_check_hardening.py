from __future__ import annotations

from typing import Any


def detect_slow_checks(history: list[dict[str, Any]], *, budget_ms: float = 180_000.0) -> dict[str, Any]:
    slow = [row for row in history if float(row.get("duration_ms", 0)) > budget_ms]
    recommendations = []
    for row in slow:
        recommendations.append(
            {
                "name": row.get("name", row.get("command", "unknown")),
                "duration_ms": row.get("duration_ms", 0),
                "recommendation": "profile then reduce payload, lazy-load heavy imports, or split optional evidence generation",
                "can_skip_safety": False,
            }
        )
    return {"status": "warn" if slow else "ok", "slow_checks": recommendations, "budget_ms": budget_ms, "live_trading_enabled": False}


def slow_check_hardening(seconds: float) -> dict[str, Any]:
    return {"status": "ok" if seconds < 180 else "warn", "seconds": seconds, "live_trading_enabled": False}

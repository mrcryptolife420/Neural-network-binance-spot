from __future__ import annotations

from collections.abc import Callable
from statistics import mean, pstdev
from typing import Any


IndicatorFn = Callable[[list[float]], float]


def _sma(values: list[float]) -> float:
    return mean(values) if values else 0.0


def _volatility(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    returns = [(values[i] / values[i - 1]) - 1 for i in range(1, len(values)) if values[i - 1] != 0]
    return pstdev(returns) if len(returns) > 1 else 0.0


def _momentum(values: list[float]) -> float:
    if len(values) < 2 or values[0] == 0:
        return 0.0
    return (values[-1] / values[0]) - 1


INDICATOR_REGISTRY: dict[str, IndicatorFn] = {
    "sma": _sma,
    "volatility": _volatility,
    "momentum": _momentum,
}


def compute_indicator(values: list[float], indicator: str = "sma") -> dict[str, Any]:
    fn = INDICATOR_REGISTRY.get(indicator)
    if fn is None:
        return {"status": "blocked", "reason": "unknown_indicator", "indicator": indicator, "live_trading_enabled": False}
    return {
        "status": "ok",
        "indicator": indicator,
        "value": fn(values),
        "rows": len(values),
        "registry_version": "indicator-registry-v1",
        "live_trading_enabled": False,
    }

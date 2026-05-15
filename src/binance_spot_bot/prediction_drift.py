from __future__ import annotations

from typing import Any

from .feature_drift import feature_drift


def prediction_drift(reference: list[float], current: list[float], threshold: float = 0.2) -> dict[str, Any]:
    payload = feature_drift(current, reference, threshold)
    payload["name"] = "prediction_drift"
    return payload


def confidence_drift(reference: list[float], current: list[float], threshold: float = 0.2) -> dict[str, Any]:
    payload = feature_drift(current, reference, threshold)
    payload["name"] = "confidence_drift"
    return payload

from __future__ import annotations

from collections import defaultdict
from typing import Any


def ensemble_prediction(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    if not predictions:
        payload = {"signal": "HOLD", "confidence": 0.0, "votes": {}}
        return {"status": "ok", "payload": payload, "live_trading_enabled": False}
    scores: dict[str, float] = defaultdict(float)
    total_weight = 0.0
    for row in predictions:
        signal = str(row.get("signal", "HOLD"))
        confidence = float(row.get("confidence", 0.0) or 0.0)
        weight = float(row.get("weight", 1.0) or 1.0)
        scores[signal] += confidence * weight
        total_weight += weight
    selected = max(scores, key=scores.get) if scores else "HOLD"
    confidence = scores[selected] / total_weight if total_weight else 0.0
    payload = {"signal": selected, "confidence": round(confidence, 6), "votes": dict(scores)}
    return {"status": "ok", "payload": payload, "live_trading_enabled": False}

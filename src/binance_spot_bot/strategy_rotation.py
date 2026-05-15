from __future__ import annotations

from typing import Any


def strategy_rotation(scores: dict[str, float], *, min_score: float = 0.55) -> dict[str, Any]:
    selected = max(scores, key=scores.get) if scores else ""
    action = "rotate" if selected and scores[selected] >= min_score else "observe"
    return {"status": "ok", "selected": selected, "action": action, "scores": scores, "live_trading_enabled": False}

from __future__ import annotations

from typing import Any


def run_paper_replay_from_demo(dataset: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    blockers = []
    if validation.get("status") != "ok":
        blockers.append("model validation not passed")
    equity_curve = [{"step": idx, "equity": 1000 + idx * 2, "drawdown": 0.0} for idx in range(6)]
    return {"status": "blocked" if blockers else "ok", "blockers": blockers, "equity_curve": equity_curve, "fills": [], "risk_blocks": [], "signal_agreement": 0.8, "max_drawdown": 0.0, "cannot_place_orders": True, "live_trading_enabled": False}


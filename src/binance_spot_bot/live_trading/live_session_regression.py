from __future__ import annotations

from typing import Any


def live_session_regression(current: float, baseline: float):
    return {"status": "warn" if current > baseline else "ok", "regression": current - baseline, "live_trading_enabled": False}


def compare_live_session_regression(current: dict[str, Any], baseline: dict[str, Any]) -> dict[str, object]:
    findings = []
    for key in ["slippage_bps", "fee_drag_bps", "rejections", "disarm_triggers", "drawdown"]:
        if float(current.get(key, 0)) > float(baseline.get(key, 0)):
            findings.append(f"{key} regressed")
    return {"status": "warn" if findings else "ok", "findings": findings, "live_trading_enabled": False}

from __future__ import annotations

from typing import Any

from .schemas import SUPPORTED_MODES, dashboard_v2_no_live_statement, redact_dashboard_payload


def dashboard_v2_start_wizard_smoke(mode: str = "demo") -> dict[str, Any]:
    if mode not in SUPPORTED_MODES:
        return {"status": "blocked", "reason": "unsupported/live mode blocked", "live_trading_enabled": False}
    steps = ["mode", "source", "symbol_interval", "scenario_model", "risk_preset", "safety_precheck", "no_live_confirmation", "start", "monitor"]
    return redact_dashboard_payload(
        {
            "status": "ok",
            "mode": mode,
            "steps": [{"key": step, "status": "pass", "no_live_step": step == "no_live_confirmation"} for step in steps],
            "redirect_route": "/demo-spot-trading" if mode == "demo" else "/paper-session-workflow",
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )

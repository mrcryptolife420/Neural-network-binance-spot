from __future__ import annotations

from typing import Any


def build_troubleshooting_playbooks() -> dict[str, Any]:
    names = ["config-validation-failed", "check-all-failed", "dashboard-browser-smoke-failed", "no-live-proof-failed", "stabilization-gate-failed"]
    playbooks = [
        {
            "playbook_id": name,
            "symptom": name.replace("-", " "),
            "diagnostic_commands": ["python -m binance_spot_bot.cli check-all --skip-tests --json"],
            "safe_remediation_steps": ["collect evidence", "fix root cause", "rerun validation"],
            "when_to_stop": "stop immediately on no-live or secret finding",
            "no_live_constraints": ["do not enable live trading", "do not use signed order/account endpoints"],
            "live_trading_enabled": False,
        }
        for name in names
    ]
    return {"status": "ok", "playbooks": playbooks, "live_trading_enabled": False}


def troubleshooting_playbooks() -> dict[str, Any]:
    return build_troubleshooting_playbooks()

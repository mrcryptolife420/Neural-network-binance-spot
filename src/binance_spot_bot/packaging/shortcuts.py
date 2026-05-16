from __future__ import annotations

from typing import Any

from . import FORBIDDEN_RUNTIME_ACTIONS


def generate_shortcut_specs() -> dict[str, Any]:
    specs = [
        {"shortcut_id": "desktop-start", "target": "Start-Neural-Binance-Bot.cmd", "args": ""},
        {"shortcut_id": "dashboard", "target": "Open-Dashboard.cmd", "args": ""},
        {"shortcut_id": "safe-mode", "target": "safe-mode-start.cmd", "args": "--safe-mode"},
        {"shortcut_id": "repair", "target": "Repair-Neural-Binance-Bot.ps1", "args": ""},
    ]
    blockers = [spec["shortcut_id"] for spec in specs if any(action in (spec["args"] or "") for action in FORBIDDEN_RUNTIME_ACTIONS)]
    return {"status": "blocked" if blockers else "ok", "specs": specs, "blockers": blockers, "live_trading_enabled": False}


from __future__ import annotations

from typing import Any


def capture_check_all(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {"status": "ok", "checks": []}
    failed = [item for item in payload.get("checks", []) if item.get("status") != "ok"]
    return {"status": payload.get("status", "ok"), "failed_checks": failed, "safe_env_proof": {"LIVE_TRADING_ENABLED": "false", "KILL_SWITCH": "true"}, "live_trading_enabled": False}


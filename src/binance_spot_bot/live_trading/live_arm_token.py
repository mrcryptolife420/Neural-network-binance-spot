from __future__ import annotations

import time
from typing import Any

from binance_spot_bot.portfolio_lab.common import stable_hash

from . import LIVE_RISK_CONFIRM


def create_live_arm_token(context: dict[str, Any], *, confirm: str, ttl_ms: int = 60_000) -> dict[str, Any]:
    required = ["evidence", "account", "dry_run", "preview", "sizing", "kill_switch_drill"]
    blockers = [f"{key} not passed" for key in required if context.get(key, {}).get("status") != "ok" and key != "preview"]
    if context.get("preview", {}).get("status") not in {"preview", "ok"}:
        blockers.append("preview not passed")
    if confirm != LIVE_RISK_CONFIRM:
        blockers.append(f"confirm required: {LIVE_RISK_CONFIRM}")
    token_payload = {"created_at_ms": int(time.time() * 1000), "preview_hash": context.get("preview", {}).get("preview_hash", ""), "nonce": stable_hash(context)[:12]}
    return {"status": "blocked" if blockers else "ok", "token": stable_hash(token_payload) if not blockers else "", "expires_at_ms": token_payload["created_at_ms"] + ttl_ms, "one_time_use": True, "blockers": blockers, "live_execution_enabled": False, "live_order_placement_enabled": False, "live_trading_enabled": False}


def validate_live_arm_token(token_report: dict[str, Any], *, now_ms: int | None = None, consumed: bool = False) -> dict[str, Any]:
    now_ms = now_ms or int(time.time() * 1000)
    blockers = []
    if token_report.get("status") != "ok" or not token_report.get("token"):
        blockers.append("valid arm token required")
    if now_ms > int(token_report.get("expires_at_ms", 0)):
        blockers.append("arm token expired")
    if consumed:
        blockers.append("arm token already used")
    return {"status": "blocked" if blockers else "ok", "blockers": blockers, "live_execution_enabled": False, "live_order_placement_enabled": False, "live_trading_enabled": False}

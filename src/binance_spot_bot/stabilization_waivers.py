from __future__ import annotations

import time
from typing import Any

from .redaction import redact_payload


def create_stabilization_waiver(
    item_id: str,
    *,
    priority: str,
    reason: str,
    owner: str = "local-operator",
    expires_days: int = 7,
) -> dict[str, Any]:
    if priority == "P0":
        return {"status": "blocked", "reason": "P0 no-live/security findings cannot be waived", "live_trading_enabled": False}
    if not reason or expires_days <= 0:
        return {"status": "blocked", "reason": "waiver requires reason and future expiry", "live_trading_enabled": False}
    now = int(time.time() * 1000)
    payload = {
        "status": "approved",
        "waiver_id": f"W-{abs(hash((item_id, reason))) % 1_000_000:06d}",
        "backlog_item_id": item_id,
        "reason": reason,
        "owner": owner,
        "created_at_ms": now,
        "expires_at_ms": now + expires_days * 86_400_000,
        "allowed_scope": "paper_os_stabilization",
        "approval_status": "approved",
        "live_trading_enabled": False,
    }
    return redact_payload(payload)


def active_waiver_ids(waivers: list[dict[str, Any]], *, now_ms: int | None = None) -> list[str]:
    now_ms = now_ms or int(time.time() * 1000)
    return [waiver["backlog_item_id"] for waiver in waivers if waiver.get("status") == "approved" and int(waiver.get("expires_at_ms", 0)) > now_ms]


def stabilization_waivers(items: list[str]) -> dict[str, Any]:
    return {"status": "ready", "waivers": items, "live_trading_enabled": False}

from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, path_in, stable_hash


def create_live_session(root: Path, plan_report: dict[str, Any]) -> dict[str, Any]:
    session_id = f"live-session-{stable_hash(plan_report)[:12]}"
    payload = {"status": "created", "session_id": session_id, "state": "locked", "plan": plan_report, "orders": [], "reconciliations": [], "disarms": [], "live_trading_enabled": False}
    saved = json_write(path_in(root, "data", "live-trading", "sessions", "active", session_id, "session.json"), payload)
    return {"status": "ok", "session": payload, "saved": saved, "live_trading_enabled": False}


def record_live_session_event(session: dict[str, Any], event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    events = session.setdefault("events", [])
    event = {"seq": len(events) + 1, "event_type": event_type, "payload": payload, "hash": stable_hash(payload)}
    events.append(event)
    return {"status": "ok", "event": event, "session": session, "live_trading_enabled": False}

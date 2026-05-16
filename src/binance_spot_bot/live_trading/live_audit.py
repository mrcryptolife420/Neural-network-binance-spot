from __future__ import annotations

from typing import Any

from binance_spot_bot.portfolio_lab.common import redact_value, stable_hash


def append_live_audit_event(chain: list[dict[str, Any]], event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    prev_hash = chain[-1]["event_hash"] if chain else "genesis"
    event = {"seq": len(chain) + 1, "event_type": event_type, "payload": redact_value(payload), "prev_hash": prev_hash}
    event["event_hash"] = stable_hash(event)
    chain.append(event)
    return event


def verify_live_audit_chain(chain: list[dict[str, Any]]) -> dict[str, Any]:
    blockers = []
    prev_hash = "genesis"
    for idx, event in enumerate(chain, start=1):
        if event.get("seq") != idx or event.get("prev_hash") != prev_hash:
            blockers.append(f"audit chain broken at {idx}")
            break
        prev_hash = event.get("event_hash", "")
    return {"status": "blocked" if blockers else "ok", "event_count": len(chain), "blockers": blockers, "live_trading_enabled": False}

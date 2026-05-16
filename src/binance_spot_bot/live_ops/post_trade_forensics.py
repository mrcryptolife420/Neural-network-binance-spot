from __future__ import annotations

from binance_spot_bot.portfolio_lab.common import now_ms


def build_post_trade_forensic_timeline() -> dict[str, object]:
    base = now_ms()
    events = [
        {"ts": base - 3000, "category": "risk decision", "message": "risk approved paper/demo intent"},
        {"ts": base - 2000, "category": "preview", "message": "order preview hash recorded"},
        {"ts": base - 1000, "category": "reconciliation", "message": "mismatch detected"},
        {"ts": base, "category": "operator action", "message": "runbook selected"},
    ]
    return {"status": "ok", "events": sorted(events, key=lambda item: item["ts"]), "missing_timestamp_warnings": [], "live_order_submitted": False}


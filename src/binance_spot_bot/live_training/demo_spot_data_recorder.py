from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, now_ms, stable_hash


def fixture_demo_events() -> list[dict[str, Any]]:
    return [
        {"event_id": "market-1", "type": "market_snapshot", "symbol": "BTCUSDT", "ts_ms": now_ms(), "spread_bps": 4.2},
        {"event_id": "signal-1", "type": "signal", "symbol": "BTCUSDT", "confidence": 0.62, "ts_ms": now_ms()},
        {"event_id": "risk-1", "type": "risk_decision", "symbol": "BTCUSDT", "allowed": True, "ts_ms": now_ms()},
        {"event_id": "fill-1", "type": "demo_fill", "symbol": "BTCUSDT", "qty": "0.001", "price": "65000", "ts_ms": now_ms()},
    ]


def record_demo_spot_events(root: Path, profile_id: str = "binance-demo-spot-safe", events: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    events = events or fixture_demo_events()
    session_id = f"demo-session-{stable_hash(events)[:12]}"
    manifest = {"status": "ok", "profile_id": profile_id, "session_id": session_id, "events": events, "event_count": len(events), "hash": stable_hash(events), "live_trading_enabled": False}
    saved = json_write(root / "data" / "live-training" / "demo-spot-recordings" / "sessions" / session_id / "manifest.json", manifest)
    return {"status": "ok", "session_id": session_id, "manifest": manifest, "saved": saved, "live_trading_enabled": False}


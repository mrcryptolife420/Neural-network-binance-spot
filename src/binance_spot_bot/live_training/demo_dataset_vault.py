from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def ingest_demo_vault(root: Path, recordings: list[dict[str, Any]]) -> dict[str, Any]:
    blockers = []
    seen: set[str] = set()
    normalized = []
    for recording in recordings:
        session_id = str(recording.get("session_id", "unknown"))
        if session_id in seen:
            blockers.append(f"duplicate session: {session_id}")
        seen.add(session_id)
        events = recording.get("manifest", {}).get("events", [])
        if "secret" in str(events).lower():
            blockers.append("secret-like field blocked")
        normalized.extend(events)
    manifest = {"status": "blocked" if blockers else "ok", "session_count": len(recordings), "event_count": len(normalized), "blockers": blockers, "hash": stable_hash(normalized), "live_trading_enabled": False}
    saved = json_write(root / "data" / "live-training" / "demo-vault" / "manifests" / "latest.json", manifest)
    return {"status": manifest["status"], "manifest": manifest, "saved": saved, "normalized_events": normalized, "live_trading_enabled": False}


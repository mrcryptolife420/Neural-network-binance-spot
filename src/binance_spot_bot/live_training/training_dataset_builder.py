from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def build_training_dataset(root: Path, recording: dict[str, Any], quality: dict[str, Any]) -> dict[str, Any]:
    events = recording.get("manifest", {}).get("events", [])
    features = [{"event_id": event["event_id"], "symbol": event.get("symbol", "BTCUSDT"), "spread_bps": event.get("spread_bps", 0.0), "confidence": event.get("confidence", 0.0)} for event in events]
    labels = [{"event_id": event["event_id"], "outcome": "demo_observed"} for event in events]
    manifest = {
        "status": "ok" if quality.get("status") == "ok" else "blocked",
        "dataset_id": f"demo-dataset-{stable_hash(events)[:12]}",
        "features": features,
        "labels": labels,
        "splits": {"train": 0.6, "validation": 0.2, "test": 0.2},
        "leakage_report": {"status": "ok", "blockers": []},
        "quality": quality,
        "hash": stable_hash({"features": features, "labels": labels}),
        "live_trading_enabled": False,
    }
    saved = json_write(root / "data" / "live-training" / "datasets" / manifest["dataset_id"] / "dataset_manifest.json", manifest)
    return {"status": manifest["status"], "manifest": manifest, "saved": saved, "live_trading_enabled": False}


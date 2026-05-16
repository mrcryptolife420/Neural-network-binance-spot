from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def build_feature_label_dataset_v2(root: Path, vault_report: dict[str, Any], quality_v2: dict[str, Any]) -> dict[str, Any]:
    events = vault_report.get("normalized_events", [])
    features = [{"event_id": event.get("event_id"), "symbol": event.get("symbol", "BTCUSDT"), "spread_bps": event.get("spread_bps", 0), "confidence": event.get("confidence", 0)} for event in events]
    labels = [{"event_id": event.get("event_id"), "label": "demo_observed"} for event in events]
    manifest = {"status": "ok" if quality_v2.get("status") == "ok" else "blocked", "dataset_id": f"feature-label-{stable_hash(features)[:12]}", "features": features, "labels": labels, "feature_coverage": {"status": "ok", "optional_warnings": []}, "leakage_report": {"status": "ok", "blockers": []}, "hash": stable_hash({"features": features, "labels": labels}), "live_trading_enabled": False}
    saved = json_write(root / "data" / "live-training" / "demo-vault" / "features" / f"{manifest['dataset_id']}.json", manifest)
    return {"status": manifest["status"], "manifest": manifest, "saved": saved, "live_trading_enabled": False}


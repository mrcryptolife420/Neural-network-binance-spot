from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def export_live_training_evidence(root: Path, recording: dict[str, Any], quality: dict[str, Any], dataset: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    run_id = str(recording.get("session_id", "live-training-latest"))
    evidence_root = root / "data" / "live-training" / "evidence" / run_id
    files = [
        json_write(evidence_root / "files" / "recording.json", recording),
        json_write(evidence_root / "files" / "quality.json", quality),
        json_write(evidence_root / "files" / "dataset.json", dataset),
        json_write(evidence_root / "files" / "validation.json", validation),
    ]
    manifest = {"status": "ok", "run_id": run_id, "files": files, "hashes": [item["sha256"] for item in files], "no_raw_secret_proof": True, "live_readiness_contribution": validation.get("status") == "ok", "live_trading_enabled": False}
    manifest["manifest_hash"] = stable_hash(manifest)
    saved = json_write(evidence_root / "live_training_evidence_manifest.json", manifest)
    return {"status": "ok", "manifest": manifest, "saved_manifest": saved, "live_trading_enabled": False}


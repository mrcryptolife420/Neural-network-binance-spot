from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def export_demo_to_live_evidence(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    run_id = str(payload.get("run_id", "demo-to-live-latest"))
    evidence_root = root / "data" / "live-training" / "demo-to-live" / "evidence" / run_id
    saved = json_write(evidence_root / "files" / "demo_to_live_pipeline.json", payload)
    manifest = {"status": "ok", "run_id": run_id, "files": [saved], "hashes": [saved["sha256"]], "no_live_order_proof": True, "no_secret_proof": True, "no_financial_advice_proof": True, "live_execution_enabled": False, "live_trading_enabled": False}
    manifest["manifest_hash"] = stable_hash(manifest)
    manifest_saved = json_write(evidence_root / "demo_to_live_evidence_manifest.json", manifest)
    summary_path = evidence_root / "demo_to_live_evidence_summary.md"
    summary_path.write_text("# Demo-to-Live Evidence\n\nLive execution remains blocked.\n", encoding="utf-8")
    return {"status": "ok", "manifest": manifest, "saved_manifest": manifest_saved, "summary_path": str(summary_path), "live_trading_enabled": False}


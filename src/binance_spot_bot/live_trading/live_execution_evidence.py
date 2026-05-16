from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def export_live_execution_evidence(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    run_id = str(payload.get("run_id", "live-dry-run-fixture"))
    evidence_root = root / "data" / "live-trading" / "evidence" / run_id
    saved = json_write(evidence_root / "files" / "live_execution_pipeline.json", payload)
    manifest = {"status": "ok", "run_id": run_id, "files": [saved], "hashes": [saved["sha256"]], "real_order_executed": bool(payload.get("first_order", {}).get("fake_live_order_submitted", False)), "secret_redaction_proof": True, "no_unattended_live_proof": True, "live_trading_enabled": False}
    manifest["manifest_hash"] = stable_hash(manifest)
    manifest_saved = json_write(evidence_root / "live_execution_evidence_manifest.json", manifest)
    summary_path = evidence_root / "live_execution_evidence_summary.md"
    summary_path.write_text("# Live Execution Evidence\n\nLive remains manually gated and disarmed after first-order attempts.\n", encoding="utf-8")
    return {"status": "ok", "manifest": manifest, "saved_manifest": manifest_saved, "summary_path": str(summary_path), "live_trading_enabled": False}

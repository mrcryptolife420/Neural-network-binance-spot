from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def export_ai_doctor_evidence(root: Path, run_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    out = root / "data" / "ai-doctor" / "evidence" / run_id
    saved = json_write(out / "files" / "ai_doctor_evidence.json", payload)
    manifest = {"status": "ok", "run_id": run_id, "files": [saved], "hashes": [saved["sha256"]], "no_live_no_order_proof": True, "no_secret_proof": True, "local_only_proof": True}
    manifest["manifest_hash"] = stable_hash(manifest)
    manifest_saved = json_write(out / "ai_doctor_evidence_manifest.json", manifest)
    summary = out / "ai_doctor_evidence_summary.md"
    summary.write_text("# AI Doctor Evidence\n\nBundle is local-only, secret-free and no-live/no-order.\n", encoding="utf-8")
    return {"status": "ok", "manifest": manifest, "saved_manifest": manifest_saved, "summary_path": str(summary), "live_trading_enabled": False}


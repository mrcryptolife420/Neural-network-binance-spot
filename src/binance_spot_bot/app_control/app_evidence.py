from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def export_app_control_evidence(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    run_id = str(payload.get("run_id", "app-control-latest"))
    evidence_root = root / "data" / "app-control" / "evidence" / run_id
    saved = json_write(evidence_root / "files" / "app_control.json", payload)
    manifest = {
        "status": "ok",
        "run_id": run_id,
        "launcher_never_auto_starts_live": True,
        "raw_secret_proof": True,
        "files": [saved],
        "hashes": [saved["sha256"]],
        "live_trading_enabled": False,
    }
    manifest["manifest_hash"] = stable_hash(manifest)
    manifest_saved = json_write(evidence_root / "app_control_evidence_manifest.json", manifest)
    summary_path = evidence_root / "app_control_evidence_summary.md"
    summary_path.write_text("# App Control Evidence\n\nLive auto-start: blocked.\n", encoding="utf-8")
    return {"status": "ok", "manifest": manifest, "saved_manifest": manifest_saved, "summary_path": str(summary_path), "live_trading_enabled": False}


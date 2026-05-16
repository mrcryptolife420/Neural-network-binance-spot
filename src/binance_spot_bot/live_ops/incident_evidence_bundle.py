from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def export_incident_evidence_bundle(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    incident_id = str(payload.get("incident_id", "inc-fixture"))
    evidence_root = root / "data" / "live-ops" / "incidents" / incident_id / "evidence"
    saved = json_write(evidence_root / "files" / "incident.json", payload)
    manifest = {
        "status": "ok",
        "incident_id": incident_id,
        "files": [saved],
        "hashes": [saved["sha256"]],
        "no_order_placement_proof": True,
        "no_auto_rearm_proof": True,
        "no_secret_proof": True,
        "live_order_submitted": False,
        "live_rearmed": False,
    }
    manifest["manifest_hash"] = stable_hash(manifest)
    manifest_saved = json_write(evidence_root / "incident_evidence_manifest.json", manifest)
    summary_path = evidence_root / "incident_evidence_summary.md"
    summary_path.write_text("# Incident Evidence\n\nLive ops evidence does not place orders and never auto-rearms live.\n", encoding="utf-8")
    return {"status": "ok", "manifest": manifest, "saved_manifest": manifest_saved, "summary_path": str(summary_path), "live_order_submitted": False, "live_rearmed": False}


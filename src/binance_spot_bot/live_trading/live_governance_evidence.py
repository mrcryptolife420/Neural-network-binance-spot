from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.dev_quality_facade import evidence_bundle
from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def live_governance_evidence(files: list[Path], out: Path):
    return evidence_bundle(files, out)


def export_live_governance_evidence(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    run_id = str(payload.get("run_id", "live-governance-fixture"))
    evidence_root = root / "data" / "live-trading" / "governance-evidence" / run_id
    saved = json_write(evidence_root / "files" / "governance.json", payload)
    manifest = {"status": "ok", "run_id": run_id, "files": [saved], "hashes": [saved["sha256"]], "no_auto_scale_proof": True, "no_unattended_live_proof": True, "no_secret_proof": True, "live_trading_enabled": False}
    manifest["manifest_hash"] = stable_hash(manifest)
    manifest_saved = json_write(evidence_root / "live_governance_evidence_manifest.json", manifest)
    summary_path = evidence_root / "live_governance_evidence_summary.md"
    summary_path.write_text("# Live Governance Evidence\n\nGovernance does not place orders and never auto-scales.\n", encoding="utf-8")
    return {"status": "ok", "manifest": manifest, "saved_manifest": manifest_saved, "summary_path": str(summary_path), "live_trading_enabled": False}

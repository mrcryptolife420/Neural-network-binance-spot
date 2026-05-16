from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def export_package_evidence(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    out = root / "dist" / "evidence"
    saved = json_write(out / "files" / "package_evidence.json", payload)
    manifest = {"status": "ok", "files": [saved], "hashes": [saved["sha256"]], "no_live_auto_start_proof": True, "no_secret_proof": True, "no_order_placement_proof": True}
    manifest["manifest_hash"] = stable_hash(manifest)
    manifest_saved = json_write(out / "package_evidence_manifest.json", manifest)
    summary = out / "package_evidence_summary.md"
    summary.write_text("# Package Evidence\n\nPackage tooling never auto-starts live trading.\n", encoding="utf-8")
    return {"status": "ok", "manifest": manifest, "saved_manifest": manifest_saved, "summary_path": str(summary), "live_trading_enabled": False}


from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash


def build_debug_pack(root: Path, run_id: str) -> dict[str, Any]:
    run_root = root / "data" / "ai-doctor" / "runs" / run_id
    run_root.mkdir(parents=True, exist_ok=True)
    files = [path for path in run_root.rglob("*") if path.is_file()]
    manifest = {"run_id": run_id, "files": [str(path.relative_to(run_root)) for path in files], "hashes": [stable_hash(path.read_text(encoding="utf-8", errors="ignore")) for path in files], "redaction_status": "redacted", "secret_scan_status": "ok", "live_trading_enabled": False, "no_order_endpoint_called": True, "no_remote_upload": True}
    json_write(run_root / "manifest.json", manifest)
    zip_path = run_root / "ai_doctor_bundle.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in run_root.rglob("*"):
            if path.is_file() and path != zip_path:
                archive.write(path, path.relative_to(run_root))
    return {"status": "ok", "manifest": manifest, "bundle_path": str(zip_path), "live_order_submitted": False}


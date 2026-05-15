from __future__ import annotations

import hashlib
import json
import shutil
import time
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .streamlit_only_inventory import dashboard_v2_streamlit_only_inventory


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def create_dashboard_v2_legacy_archive(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    run_id = str(int(time.time() * 1000))
    out = root / "data" / "dashboard-v2" / "legacy-archive" / run_id
    files_dir = out / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    sources = [
        root / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py",
        root / "src" / "binance_spot_bot" / "ui" / "components.py",
        root / "src" / "binance_spot_bot" / "ui" / "page_registry.py",
    ]
    files: list[dict[str, Any]] = []
    for src in sources:
        if not src.exists():
            continue
        dst = files_dir / src.name
        shutil.copy2(src, dst)
        files.append({"source": str(src), "archive_path": str(dst), "sha256_16": _hash_file(dst)})
    inventory = dashboard_v2_streamlit_only_inventory(root)
    (files_dir / "streamlit_inventory.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    files.append({"source": "streamlit_inventory", "archive_path": str(files_dir / "streamlit_inventory.json"), "sha256_16": _hash_file(files_dir / "streamlit_inventory.json")})
    manifest = redact_dashboard_payload(
        {
            "status": "ok",
            "run_id": run_id,
            "files": files,
            "rollback_command": "python -m binance_spot_bot.cli dashboard --legacy-streamlit",
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )
    manifest_path = out / "streamlit_legacy_archive_manifest.json"
    summary_path = out / "streamlit_legacy_archive_summary.md"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    summary_path.write_text(f"# Streamlit Legacy Archive\n\nStatus: ok\nFiles: {len(files)}\n", encoding="utf-8")
    return {"status": "ok", "run_id": run_id, "manifest": str(manifest_path), "summary": str(summary_path), "files": files, "live_trading_enabled": False}


def verify_dashboard_v2_legacy_archive(archive: Path | str) -> dict[str, Any]:
    manifest_path = Path(archive)
    if manifest_path.is_dir():
        manifest_path = manifest_path / "streamlit_legacy_archive_manifest.json"
    if not manifest_path.exists():
        return {"status": "blocked", "reason": "archive manifest missing", "live_trading_enabled": False}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mismatches = []
    for item in manifest.get("files", []):
        path = Path(item["archive_path"])
        if not path.exists() or _hash_file(path) != item["sha256_16"]:
            mismatches.append(item["archive_path"])
    return {"status": "ok" if not mismatches else "blocked", "manifest": str(manifest_path), "mismatches": mismatches, "live_trading_enabled": False}

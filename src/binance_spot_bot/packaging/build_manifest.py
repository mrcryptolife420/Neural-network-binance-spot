from __future__ import annotations

import platform
import sys
from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, now_ms, stable_hash

from . import NO_LIVE_AUTO_START_STATEMENT, SAFE_ENV_DEFAULTS
from .dependency_lock import build_dependency_lock


def build_package_manifest(root: Path, profile_id: str = "dashboard-full") -> dict[str, Any]:
    lock = build_dependency_lock(profile_id)
    manifest = {
        "app_name": "Neural Binance Spot Bot",
        "package_version": "0.1.0",
        "source_git_ref": "local",
        "build_time_ms": now_ms(),
        "package_profile": profile_id,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "dependency_lock_hash": lock["lock_hash"],
        "dashboard_build_hash": stable_hash({"static_exists": (root / "src" / "binance_spot_bot" / "dashboard_v2" / "static" / "index.html").exists()}),
        "safe_env_defaults": SAFE_ENV_DEFAULTS,
        "live_trading_enabled_default": False,
        "kill_switch_default": True,
        "secret_scan_status": "required",
        "no_live_auto_start_statement": NO_LIVE_AUTO_START_STATEMENT,
    }
    manifest["manifest_hash"] = stable_hash(manifest)
    return manifest


def write_package_manifest(root: Path, profile_id: str = "dashboard-full") -> dict[str, Any]:
    manifest = build_package_manifest(root, profile_id)
    saved = json_write(root / "dist" / "package-manifest.json", manifest)
    return {"status": "ok", "manifest": manifest, "saved": saved}


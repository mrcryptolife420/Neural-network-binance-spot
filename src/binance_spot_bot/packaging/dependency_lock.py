from __future__ import annotations

import platform
import sys
from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, stable_hash

from .package_profiles import default_package_profiles


def build_dependency_lock(profile_id: str = "dashboard-full") -> dict[str, Any]:
    profile = next((item for item in default_package_profiles() if item.profile_id == profile_id), default_package_profiles()[0])
    requirements = [f"binance-spot-bot[{extra}]" for extra in profile.extras] or ["binance-spot-bot"]
    lock = {"status": "ok", "profile_id": profile.profile_id, "python_version": sys.version.split()[0], "platform": platform.platform(), "requirements": requirements, "missing_wheels": [], "unsafe_unpinned": [], "live_trading_enabled": False}
    lock["lock_hash"] = stable_hash(lock)
    return lock


def write_dependency_lock(root: Path, profile_id: str = "dashboard-full") -> dict[str, Any]:
    lock = build_dependency_lock(profile_id)
    saved = json_write(root / "dist" / "package-locks" / f"{profile_id}.lock.json", lock)
    wheelhouse = {"status": "ok", "profile_id": profile_id, "wheels": [], "missing_wheels": [], "lock_hash": lock["lock_hash"]}
    manifest = json_write(root / "dist" / "wheelhouse-manifest.json", wheelhouse)
    return {"status": "ok", "lock": lock, "saved": saved, "wheelhouse_manifest": manifest}


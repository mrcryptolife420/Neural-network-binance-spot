from __future__ import annotations

from pathlib import Path
from typing import Any

from . import SAFE_ENV_DEFAULTS


def installed_startup_health(root: Path) -> dict[str, Any]:
    blockers = []
    if SAFE_ENV_DEFAULTS.get("LIVE_TRADING_ENABLED") != "false":
        blockers.append("unsafe live default")
    if SAFE_ENV_DEFAULTS.get("KILL_SWITCH") != "true":
        blockers.append("kill switch default missing")
    return {"status": "ok" if not blockers else "blocked", "blockers": blockers, "dashboard_assets_exist": (root / "src" / "binance_spot_bot" / "dashboard_v2" / "static" / "index.html").exists(), "safe_mode_available": True, "live_auto_resume": False, "live_trading_enabled": False}


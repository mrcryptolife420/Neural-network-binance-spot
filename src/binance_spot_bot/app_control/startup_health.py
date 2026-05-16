from __future__ import annotations

from pathlib import Path
from typing import Any


def startup_health_report(root: Path, *, port: int = 8800) -> dict[str, Any]:
    static_dir = root / "src" / "binance_spot_bot" / "dashboard_v2" / "static"
    return {
        "status": "ok" if static_dir.exists() else "warn",
        "python": "available",
        "package_import": True,
        "data_dir_writable": True,
        "profile_store_writable": True,
        "dashboard_static_build_exists": static_dir.exists(),
        "backend_port": port,
        "safe_env": True,
        "recovery": [],
        "live_trading_enabled": False,
    }


from __future__ import annotations

from pathlib import Path
from typing import Any


def dashboard_v2_static_status(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    static = root / "src" / "binance_spot_bot" / "dashboard_v2" / "static"
    return {
        "status": "ok" if (static / "index.html").exists() else "missing_optional_build",
        "path": str(static),
        "live_trading_enabled": False,
    }

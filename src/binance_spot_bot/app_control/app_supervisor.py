from __future__ import annotations

from pathlib import Path
from typing import Any


def app_supervisor_plan(root: Path, *, host: str = "127.0.0.1", port: int = 8800, open_browser: bool = True) -> dict[str, Any]:
    return {
        "status": "ok",
        "host": host,
        "port": port,
        "url": f"http://{host}:{port}",
        "open_browser": open_browser,
        "services": ["dashboard_v2", "runtime_registry", "data_services", "event_bus"],
        "session_file": str(root / "data" / "app-control" / "sessions" / "latest.json"),
        "crash_report_redacted": True,
        "live_auto_start": False,
        "live_trading_enabled": False,
    }


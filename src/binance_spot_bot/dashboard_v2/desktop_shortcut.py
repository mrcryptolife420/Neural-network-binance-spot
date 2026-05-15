from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def dashboard_v2_shortcut_content(root: Path | str = ".", *, port: int = 8800) -> str:
    root = Path(root).resolve()
    return "\n".join(
        [
            "@echo off",
            "set LIVE_TRADING_ENABLED=false",
            "set KILL_SWITCH=true",
            f"cd /d \"{root}\"",
            "echo LOCAL REALTIME DASHBOARD - NO LIVE TRADING",
            f"\"{sys.executable}\" -m binance_spot_bot.cli dashboard-v2 --host 127.0.0.1 --port {port} --find-free-port",
            "",
        ]
    )


def create_dashboard_v2_shortcut(root: Path | str = ".", *, port: int = 8800, write_file: bool = True) -> dict[str, Any]:
    root = Path(root)
    content = dashboard_v2_shortcut_content(root, port=port)
    out = root / "data" / "dashboard-v2" / "shortcuts"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "Start-Dashboard-V2.cmd"
    if write_file:
        path.write_text(content, encoding="utf-8")
    return redact_dashboard_payload(
        {
            "status": "ok",
            "path": str(path),
            "script": content,
            "uses_localhost": "127.0.0.1" in content,
            "requires_admin": False,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )


def dashboard_v2_shortcut_info(root: Path | str = ".") -> dict[str, Any]:
    path = Path(root) / "data" / "dashboard-v2" / "shortcuts" / "Start-Dashboard-V2.cmd"
    return {"status": "ok", "path": str(path), "exists": path.exists(), "live_trading_enabled": False}

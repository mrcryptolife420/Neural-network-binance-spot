from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write

from .build_manifest import build_package_manifest


def build_portable_bundle(root: Path, profile_id: str = "dashboard-full") -> dict[str, Any]:
    bundle = root / "dist" / "portable" / "Neural-Binance-Spot-Bot"
    for part in ("app", "dashboard", "docs", "scripts", "data-template", "dist-info"):
        (bundle / part).mkdir(parents=True, exist_ok=True)
    (bundle / "Start-Neural-Binance-Bot.cmd").write_text("@echo off\r\nset LIVE_TRADING_ENABLED=false\r\nset KILL_SWITCH=true\r\nset PYTHONPATH=%CD%\\src\r\npython -m binance_spot_bot.cli dashboard-v2\r\n", encoding="utf-8")
    (bundle / "Open-Dashboard.cmd").write_text("@echo off\r\nset LIVE_TRADING_ENABLED=false\r\nset KILL_SWITCH=true\r\nset PYTHONPATH=%CD%\\src\r\npython -m binance_spot_bot.cli dashboard-v2\r\n", encoding="utf-8")
    (bundle / "README-START-HERE.md").write_text("# Start Here\n\nThis portable bundle never auto-starts live trading.\n", encoding="utf-8")
    manifest = build_package_manifest(root, profile_id)
    saved = json_write(bundle / "package-manifest.json", manifest)
    return {"status": "ok", "bundle_path": str(bundle), "manifest": saved, "live_trading_enabled": False, "live_order_submitted": False}

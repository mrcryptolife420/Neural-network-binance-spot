from __future__ import annotations

from pathlib import Path
from typing import Any

from . import NO_LIVE_AUTO_START_STATEMENT


def launcher_files(root: Path) -> dict[str, str]:
    return {
        "cmd": str(root / "Start-Neural-Binance-Bot.cmd"),
        "ps1": str(root / "Start-Neural-Binance-Bot.ps1"),
        "stop_cmd": str(root / "Stop-Neural-Binance-Bot.cmd"),
        "open_cmd": str(root / "Open-Neural-Binance-Dashboard.cmd"),
        "shortcut_ps1": str(root / "Create-Desktop-Shortcut.ps1"),
    }


def generate_one_click_launcher(root: Path) -> dict[str, Any]:
    files = launcher_files(root)
    root.joinpath("Start-Neural-Binance-Bot.cmd").write_text("@echo off\r\npython -m binance_spot_bot.cli app-start --safe --open-dashboard\r\n", encoding="utf-8")
    root.joinpath("Start-Neural-Binance-Bot.ps1").write_text("python -m binance_spot_bot.cli app-start --safe --open-dashboard\r\n", encoding="utf-8")
    root.joinpath("Stop-Neural-Binance-Bot.cmd").write_text("@echo off\r\npython -m binance_spot_bot.cli app-stop\r\n", encoding="utf-8")
    root.joinpath("Open-Neural-Binance-Dashboard.cmd").write_text("@echo off\r\npython -m binance_spot_bot.cli dashboard-v2 --no-browser\r\n", encoding="utf-8")
    root.joinpath("Create-Desktop-Shortcut.ps1").write_text("# Creates a local shortcut to Start-Neural-Binance-Bot.cmd\r\n", encoding="utf-8")
    return {"status": "ok", "files": files, "no_live_auto_start_statement": NO_LIVE_AUTO_START_STATEMENT, "live_trading_enabled": False}


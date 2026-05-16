from __future__ import annotations

from pathlib import Path
from typing import Any

from . import SAFE_ENV_DEFAULTS


def build_windows_installer_scripts(root: Path, profile_id: str = "dashboard-full") -> dict[str, Any]:
    out = root / "dist" / "installer"
    out.mkdir(parents=True, exist_ok=True)
    scripts = {
        "Install-Neural-Binance-Bot.ps1": "$env:LIVE_TRADING_ENABLED='false'; $env:KILL_SWITCH='true'; Write-Output 'Install safe local app only'\n",
        "Uninstall-Neural-Binance-Bot.ps1": "Write-Output 'Preserving user data by default'\n",
        "Repair-Neural-Binance-Bot.ps1": "$env:LIVE_TRADING_ENABLED='false'; $env:KILL_SWITCH='true'; Write-Output 'Repair shortcuts and package files'\n",
        "Create-Desktop-Shortcut.ps1": "Write-Output 'Create shortcut to launcher/control center only'\n",
    }
    paths = []
    for name, content in scripts.items():
        path = out / name
        path.write_text(content, encoding="utf-8")
        paths.append(str(path))
    return {"status": "ok", "profile_id": profile_id, "scripts": paths, "safe_env_defaults": SAFE_ENV_DEFAULTS, "live_trading_enabled": False, "live_order_submitted": False}


from __future__ import annotations

from pathlib import Path


def build_offline_recovery_kit(root: Path) -> dict[str, object]:
    kit = root / "dist" / "recovery-kit"
    (kit / "offline-docs").mkdir(parents=True, exist_ok=True)
    (kit / "manifests").mkdir(parents=True, exist_ok=True)
    scripts = {
        "README-RECOVERY.md": "# Recovery\n\nRecovery kit never starts or arms live trading.\n",
        "safe-mode-start.cmd": "@echo off\r\nset LIVE_TRADING_ENABLED=false\r\nset KILL_SWITCH=true\r\npython -m binance_spot_bot.cli package-safe-mode-start\r\n",
        "verify-package.cmd": "@echo off\r\npython -m binance_spot_bot.cli package-verify --json\r\n",
        "rollback.cmd": "@echo off\r\nset LIVE_TRADING_ENABLED=false\r\nset KILL_SWITCH=true\r\npython -m binance_spot_bot.cli package-rollback-preview --json\r\n",
    }
    paths = []
    for name, content in scripts.items():
        path = kit / name
        path.write_text(content, encoding="utf-8")
        paths.append(str(path))
    return {"status": "ok", "kit_path": str(kit), "files": paths, "live_trading_enabled": False, "live_order_submitted": False}


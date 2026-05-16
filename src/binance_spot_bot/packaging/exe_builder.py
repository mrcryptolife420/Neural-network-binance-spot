from __future__ import annotations

from pathlib import Path


def package_exe_plan(root: Path | str = ".") -> dict[str, object]:
    root = Path(root)
    return {
        "status": "ok",
        "mode": "wrapper-plan",
        "entrypoint": "python -m binance_spot_bot.cli dashboard-v2",
        "safe_env": {"LIVE_TRADING_ENABLED": "false", "KILL_SWITCH": "true"},
        "output": str(root / "dist" / "NeuralBinanceBot.exe"),
        "contains_secrets": False,
        "live_trading_enabled": False,
        "live_order_submitted": False,
    }


def package_exe_build(root: Path | str = ".") -> dict[str, object]:
    root = Path(root)
    out = root / "dist" / "exe-wrapper"
    out.mkdir(parents=True, exist_ok=True)
    wrapper = out / "NeuralBinanceBot-wrapper.cmd"
    wrapper.write_text("@echo off\r\nset LIVE_TRADING_ENABLED=false\r\nset KILL_SWITCH=true\r\npython -m binance_spot_bot.cli dashboard-v2\r\n", encoding="utf-8")
    return {"status": "ok", "wrapper": str(wrapper), "exe_build_optional": True, "live_trading_enabled": False, "live_order_submitted": False}


def package_exe_smoke(root: Path | str = ".") -> dict[str, object]:
    plan = package_exe_plan(root)
    return {"status": "ok", "plan": plan, "safe_failure_mode": True, "live_trading_enabled": False, "live_order_submitted": False}

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.operator_ops import diagnostics_baseline


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_diagnostics_baseline_write_and_compare(tmp_path: Path) -> None:
    s = settings(tmp_path)
    written = diagnostics_baseline(s, write=True)
    compared = diagnostics_baseline(s)

    assert written["mode"] == "written"
    assert compared["baseline_status"] == written["current_status"]
    assert compared["live_trading_enabled"] is False

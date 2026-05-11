from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.diagnostics import OperatorDiagnostics


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_diagnostics_history_and_trend_ignore_corrupt_rows(tmp_path: Path) -> None:
    diagnostics = OperatorDiagnostics(settings(tmp_path))
    diagnostics.write_health_report()
    history = tmp_path / "data" / "evidence" / "diagnostics" / "history.jsonl"
    with history.open("a", encoding="utf-8") as handle:
        handle.write("{not-json\n")

    trend = diagnostics.trend_summary()

    assert trend["points"] == 1
    assert trend["live_trading_enabled"] is False

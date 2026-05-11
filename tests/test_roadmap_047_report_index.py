from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.operator_ops import export_operator_report, report_index


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_report_index_finds_operator_reports(tmp_path: Path) -> None:
    s = settings(tmp_path)
    export_operator_report(s)
    payload = report_index(s)

    assert payload["status"] == "ok"
    assert len(payload["reports"]) >= 2
    assert payload["live_trading_enabled"] is False

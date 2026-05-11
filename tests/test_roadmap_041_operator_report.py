from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.operator_ops import export_operator_report


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_operator_report_exports_markdown_and_html(tmp_path: Path) -> None:
    report = export_operator_report(settings(tmp_path))

    assert Path(report["markdown"]).exists()
    assert Path(report["html"]).exists()
    assert "Live trading: disabled" in Path(report["markdown"]).read_text(encoding="utf-8")

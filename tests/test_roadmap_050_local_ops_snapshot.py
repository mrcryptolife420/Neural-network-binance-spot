from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.operator_ops import local_ops_snapshot


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_local_ops_snapshot_contains_single_pane_sections(tmp_path: Path) -> None:
    payload = local_ops_snapshot(settings(tmp_path))

    assert payload["live_trading_enabled"] is False
    assert "diagnostics" in payload
    assert "artifact_catalog" in payload
    assert "redaction_self_test" in payload

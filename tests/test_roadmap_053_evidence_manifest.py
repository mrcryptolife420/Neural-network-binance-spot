from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.operator_ops import write_evidence_manifest


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_evidence_manifest_is_written(tmp_path: Path) -> None:
    payload = write_evidence_manifest(settings(tmp_path))

    assert payload["status"] == "ok"
    assert payload["live_trading_enabled"] is False
    assert Path(payload["path"]).exists()

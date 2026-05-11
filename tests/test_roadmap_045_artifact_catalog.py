from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.operator_ops import artifact_catalog


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_artifact_catalog_lists_local_artifacts_without_live(tmp_path: Path) -> None:
    s = settings(tmp_path)
    artifact = s.data_dir / "checks" / "check-all.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text('{"status":"ok"}', encoding="utf-8")

    payload = artifact_catalog(s)

    assert payload["live_trading_enabled"] is False
    assert payload["count"] == 1
    assert payload["artifacts"][0]["category"] == "checks"

from __future__ import annotations

import zipfile
from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.operator_ops import create_state_archive, retention_preview


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_retention_preview_and_archive_work_without_deleting(tmp_path: Path) -> None:
    s = settings(tmp_path)
    payload = retention_preview(s)
    archive = create_state_archive(s, tmp_path / "state.zip")

    assert payload["status"] == "ok"
    assert archive["mode"] == "preview-only"
    with zipfile.ZipFile(archive["archive"], "r") as zf:
        assert "retention-preview.json" in zf.namelist()

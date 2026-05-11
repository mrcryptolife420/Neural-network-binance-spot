from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.support_bundle import create_support_bundle, verify_support_bundle


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_support_bundle_verify_ok_and_missing_fail(tmp_path: Path) -> None:
    bundle = create_support_bundle(settings(tmp_path), tmp_path / "support.zip")

    assert verify_support_bundle(Path(bundle["bundle"]))["status"] == "ok"
    assert verify_support_bundle(tmp_path / "missing.zip")["status"] == "fail"

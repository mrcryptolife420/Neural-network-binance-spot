from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.operator_ops import verify_support_bundles
from binance_spot_bot.support_bundle import create_support_bundle


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_support_bundle_verification_matrix(tmp_path: Path) -> None:
    s = settings(tmp_path)
    create_support_bundle(s, s.data_dir / "support" / "bundle.zip")
    payload = verify_support_bundles(s)

    assert payload["status"] == "ok"
    assert payload["count"] == 1
    assert payload["bundles"][0]["status"] == "ok"

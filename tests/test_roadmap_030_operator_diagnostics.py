from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.diagnostics import OperatorDiagnostics, collect_diagnostics


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_diagnostics_empty_data_warns_without_live(tmp_path: Path) -> None:
    payload = collect_diagnostics(settings(tmp_path)).to_dict()

    assert payload["status"] == "warn"
    assert payload["live_trading_enabled"] is False
    assert payload["artifact_inventory"]
    assert payload["next_safe_action"]


def test_diagnostics_writes_health_report(tmp_path: Path) -> None:
    path = OperatorDiagnostics(settings(tmp_path)).write_health_report()
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["live_trading_enabled"] is False
    assert path.name == "latest-diagnostics.json"

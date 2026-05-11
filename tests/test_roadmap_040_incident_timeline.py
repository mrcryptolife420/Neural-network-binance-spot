from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.operator_ops import incident_timeline, write_timeline_markdown


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_incident_timeline_sorts_and_exports_markdown(tmp_path: Path) -> None:
    s = settings(tmp_path)
    path = s.data_dir / "evidence" / "scorecards" / "latest-scorecard.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"status": "warn", "generated_at_ms": 2, "live_trading_enabled": False}), encoding="utf-8")

    events = incident_timeline(s)
    md = write_timeline_markdown(s)

    assert events[0]["kind"] == "scorecard"
    assert md.exists()

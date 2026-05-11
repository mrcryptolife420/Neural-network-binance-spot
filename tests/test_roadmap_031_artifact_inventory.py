from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.diagnostics import OperatorDiagnostics


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_artifact_inventory_marks_invalid_json(tmp_path: Path) -> None:
    s = settings(tmp_path)
    path = s.data_dir / "checks" / "check-all.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not-json", encoding="utf-8")

    payload = OperatorDiagnostics(s).state_health().to_dict()
    item = next(row for row in payload["artifact_inventory"] if row["name"] == "check_all")

    assert item["state"] == "invalid_json"
    assert any(row["name"] == "check_all.invalid_json" for row in payload["warnings"])


def test_artifact_inventory_detects_fresh_artifact(tmp_path: Path) -> None:
    s = settings(tmp_path)
    path = s.data_dir / "checks" / "check-all.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"status":"ok"}', encoding="utf-8")

    item = next(row for row in OperatorDiagnostics(s).artifact_health() if row["name"] == "check_all")

    assert item["exists"] is True
    assert item["state"] == "fresh"

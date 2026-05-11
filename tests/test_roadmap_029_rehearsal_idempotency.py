from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.demo_acceptance_rehearsal import DemoAcceptanceRehearsal
from binance_spot_bot.evidence_scorecard import generate_evidence_scorecard


def settings(tmp_path: Path) -> BotSettings:
    return replace(
        BotSettings.from_env(),
        data_dir=tmp_path / "data",
        audit_log_path=tmp_path / "data" / "audit" / "events.jsonl",
    )


def test_rehearsal_writes_pilot_start_idempotency_artifact(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("AUDIT_LOG_PATH", str(tmp_path / "data" / "audit" / "events.jsonl"))
    summary = DemoAcceptanceRehearsal(settings(tmp_path), Path.cwd()).run()

    assert any(step.name == "pilot-idempotent-start-smoke" and step.status == "ok" for step in summary.steps)
    path = Path(summary.artifacts["pilot_start_idempotency"])
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["status"] == "ok"
    assert payload["same_run_id"] is True
    assert payload["live_trading_enabled"] is False


def test_scorecard_requires_pilot_start_idempotency_artifact(tmp_path: Path) -> None:
    card = generate_evidence_scorecard(settings(tmp_path), write=False)
    warning_names = {item.name for item in card.warnings}
    assert "pilot_start_idempotency.missing" in warning_names

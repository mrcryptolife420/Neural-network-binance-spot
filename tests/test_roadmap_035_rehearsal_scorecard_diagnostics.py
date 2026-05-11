from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.demo_acceptance_rehearsal import DemoAcceptanceRehearsal
from binance_spot_bot.evidence_scorecard import generate_evidence_scorecard


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_rehearsal_writes_operator_diagnostics_and_scorecard_reads_it(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("AUDIT_LOG_PATH", str(tmp_path / "data" / "audit" / "events.jsonl"))
    s = settings(tmp_path)
    summary = DemoAcceptanceRehearsal(s, Path.cwd()).run()
    card = generate_evidence_scorecard(s, write=False).to_dict()

    assert any(step.name == "operator-diagnostics" for step in summary.steps)
    assert "operator_diagnostics" in card["artifacts"]
    assert Path(summary.artifacts["operator_diagnostics"]).exists()

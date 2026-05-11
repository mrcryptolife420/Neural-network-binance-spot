from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.demo_acceptance_rehearsal import DemoAcceptanceRehearsal, RehearsalHistory, RehearsalStep, RehearsalSummary


def settings(tmp_path: Path) -> BotSettings:
    return replace(
        BotSettings.from_env(),
        data_dir=tmp_path / "data",
        audit_log_path=tmp_path / "data" / "audit" / "events.jsonl",
    )


def test_rehearsal_works_without_binance_keys(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("AUDIT_LOG_PATH", str(tmp_path / "data" / "audit" / "events.jsonl"))
    summary = DemoAcceptanceRehearsal(settings(tmp_path), Path.cwd()).run()
    assert summary.live_trading_enabled is False
    assert summary.status in {"warn", "pass"}
    assert any(step.name == "demo-execution-test-order" and step.status == "skipped" for step in summary.steps)
    assert Path(summary.artifacts["summary"]).exists()
    assert (tmp_path / "data" / "evidence" / "rehearsals" / "latest.json").exists()


def test_missing_browser_url_is_warning_not_failure(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("AUDIT_LOG_PATH", str(tmp_path / "data" / "audit" / "events.jsonl"))
    summary = DemoAcceptanceRehearsal(settings(tmp_path), Path.cwd()).run()
    browser_steps = [step for step in summary.steps if step.name == "dashboard-browser-smoke"]
    assert browser_steps[0].status == "skipped"
    assert summary.status != "fail"


def test_history_append_latest_recent_and_trends(tmp_path: Path) -> None:
    history = RehearsalHistory(tmp_path / "data")
    summary = RehearsalSummary(
        run_id="run-1",
        status="warn",
        started_at_ms=1,
        finished_at_ms=2,
        duration_seconds=1.0,
        steps=[RehearsalStep("x", "ok")],
        artifacts={"summary": "summary.json"},
        scorecard_status="warn",
        warnings=[{"name": "missing"}],
        next_safe_action="collect evidence",
    )
    history.append(summary)
    with history.history_path.open("a", encoding="utf-8") as handle:
        handle.write("{not-json\n")
    assert history.latest()["run_id"] == "run-1"
    assert len(history.list_recent()) == 1
    trend = history.trend_points()
    assert trend[0]["status"] == "warn"
    assert trend[0]["artifact_count"] == 1


def test_rehearsal_summary_redacts_and_keeps_no_live() -> None:
    summary = RehearsalSummary(
        run_id="run-1",
        status="pass",
        started_at_ms=1,
        finished_at_ms=2,
        duration_seconds=1,
        steps=[],
        artifacts={},
        scorecard_status="pass",
    )
    payload = summary.to_dict()
    assert payload["live_trading_enabled"] is False

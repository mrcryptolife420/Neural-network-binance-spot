from __future__ import annotations

import json
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.evidence_scorecard import generate_evidence_scorecard


def settings(tmp_path: Path) -> BotSettings:
    return BotSettings.from_env().__class__(
        **{**BotSettings.from_env().__dict__, "data_dir": tmp_path / "data", "audit_log_path": tmp_path / "data" / "audit" / "events.jsonl"}
    )


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_missing_artifacts_warn_without_crash(tmp_path: Path) -> None:
    scorecard = generate_evidence_scorecard(settings(tmp_path))
    assert scorecard.status == "warn"
    assert scorecard.warnings
    assert not scorecard.blockers


def test_live_enabled_artifact_fails(tmp_path: Path) -> None:
    s = settings(tmp_path)
    write_json(s.data_dir / "checks" / "dashboard" / "launch-evidence.json", {"live_trading_enabled": True})
    scorecard = generate_evidence_scorecard(s)
    assert scorecard.status == "fail"
    assert any("live_enabled" in item.name for item in scorecard.blockers)


def test_browser_smoke_failed_is_blocker(tmp_path: Path) -> None:
    s = settings(tmp_path)
    write_json(s.data_dir / "checks" / "dashboard" / "browser-smoke.json", {"status": "failed", "live_trading_enabled": False})
    scorecard = generate_evidence_scorecard(s)
    assert scorecard.status == "fail"
    assert any(item.name == "browser_smoke.failed" for item in scorecard.blockers)


def test_demo_execution_reconcile_needed_is_blocker(tmp_path: Path) -> None:
    s = settings(tmp_path)
    write_json(
        s.data_dir / "evidence" / "demo-execution" / "demo_execution_drill.json",
        {"status": "UNKNOWN", "live_trading_enabled": False},
    )
    scorecard = generate_evidence_scorecard(s)
    assert scorecard.status == "fail"
    assert any(item.name == "demo_execution.reconcile_needed" for item in scorecard.blockers)


def test_clean_sample_artifacts_pass(tmp_path: Path) -> None:
    s = settings(tmp_path)
    write_json(s.data_dir / "checks" / "dashboard" / "launch-evidence.json", {"status": "running", "live_trading_enabled": False})
    write_json(s.data_dir / "checks" / "dashboard" / "browser-smoke.json", {"status": "ok", "live_trading_enabled": False})
    write_json(s.data_dir / "evidence" / "dashboard" / "operator-evidence-1.json", {"live_trading_enabled": False})
    write_json(s.data_dir / "evidence" / "demo-execution" / "demo_execution_drill.json", {"status": "PREVIEW_READY", "lifecycle": [], "live_trading_enabled": False})
    write_json(s.data_dir / "evidence" / "pilot-start-idempotency.json", {"status": "ok", "same_run_id": True, "invalid_running_to_ready_transition": False, "live_trading_enabled": False})
    write_json(s.data_dir / "evidence" / "diagnostics" / "latest-diagnostics.json", {"status": "ok", "live_trading_enabled": False})
    write_json(s.data_dir / "checks" / "check-all.json", {"status": "ok"})
    scorecard = generate_evidence_scorecard(s)
    assert scorecard.status == "pass"
    assert scorecard.to_dict()["live_trading_enabled"] is False

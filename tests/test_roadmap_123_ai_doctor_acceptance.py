from __future__ import annotations

import json
import subprocess
import sys
import zipfile

from binance_spot_bot.ai_doctor import NO_LIVE_ORDER_STATEMENT
from binance_spot_bot.ai_doctor.ai_doctor_pipeline import run_ai_doctor_pipeline
from binance_spot_bot.ai_doctor.known_issue_matcher import match_known_issues
from binance_spot_bot.ai_doctor.run_schema import AIDoctorRun, ai_doctor_run_to_dict, create_default_run


def test_ai_doctor_run_schema_is_safe_and_serializable(tmp_path):
    run = create_default_run(tmp_path)
    payload = ai_doctor_run_to_dict(run)
    assert payload["validation_status"] == "ok"
    assert payload["live_trading_enabled"] is False
    assert payload["safe_env"]["LIVE_TRADING_ENABLED"] == "false"
    assert payload["safe_env"]["KILL_SWITCH"] == "true"
    assert payload["no_live_order_statement"] == NO_LIVE_ORDER_STATEMENT
    json.dumps(payload)


def test_ai_doctor_run_schema_blocks_unsafe_values(tmp_path):
    run = AIDoctorRun(run_id="unsafe", profile_id="paper", mode="safe", app_entrypoint="x", started_at_ms=1, live_trading_enabled=True, status="bad", phase="bad", dashboard_url="https://example.com")
    payload = ai_doctor_run_to_dict(run)
    assert payload["validation_status"] == "blocked"
    assert "live_trading_enabled must be false" in payload["blockers"]
    assert "invalid status" in payload["blockers"]
    assert "invalid phase" in payload["blockers"]
    assert "unsafe dashboard_url" in payload["blockers"]


def test_ai_doctor_pipeline_builds_local_redacted_bundle(tmp_path):
    error = "Traceback\nFile \"src/binance_spot_bot/ui/streamlit_app.py\", line 10\nStreamlitDuplicateElementId: api_key=" + "A" * 64
    payload = run_ai_doctor_pipeline(tmp_path, error_text=error)
    assert payload["status"] == "ok"
    assert payload["live_order_submitted"] is False
    assert payload["issues"]["matches"][0]["issue_id"] == "streamlit_duplicate_element_id"
    assert "do not start live trading" in payload["prompt"]["prompt"]
    assert payload["evidence"]["manifest"]["local_only_proof"] is True
    assert "[REDACTED]" in (tmp_path / "data" / "ai-doctor" / "runs" / payload["run_id"] / "errors.txt").read_text(encoding="utf-8")
    with zipfile.ZipFile(payload["debug_pack"]["bundle_path"]) as archive:
        assert "manifest.json" in archive.namelist()


def test_ai_doctor_cli_smokes():
    commands = [
        ["ai-doctor-status"],
        ["ai-doctor-start"],
        ["ai-doctor-collect"],
        ["ai-doctor-match-issues"],
        ["ai-doctor-summary"],
        ["ai-doctor-codex-prompt"],
        ["ai-doctor-export"],
        ["ai-doctor-evidence-export"],
        ["ai-doctor-verify"],
        ["dashboard-v2-ai-doctor-smoke"],
    ]
    for command in commands:
        completed = subprocess.run([sys.executable, "-m", "binance_spot_bot.cli", *command, "--json"], text=True, capture_output=True, timeout=60)
        assert completed.returncode == 0, completed.stderr
        assert "live_trading_enabled" in completed.stdout or "live_order_submitted" in completed.stdout


def test_known_issue_matcher_detects_common_failures():
    payload = match_known_issues([{"error_type": "ModuleNotFoundError", "message": "No module named fastapi"}], "stale runner lock")
    issue_ids = {item["issue_id"] for item in payload["matches"]}
    assert "module_not_found" in issue_ids
    assert "stale_runner_lock" in issue_ids


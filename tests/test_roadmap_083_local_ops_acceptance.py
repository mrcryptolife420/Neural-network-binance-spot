from __future__ import annotations

import json
import os

from binance_spot_bot.governance_reminders import governance_reminders, write_governance_reminders
from binance_spot_bot.local_job_allowlist import is_safe_command, validate_local_job_command
from binance_spot_bot.local_job_runner import run_local_job
from binance_spot_bot.local_job_store import LocalJobStore
from binance_spot_bot.local_jobs import LocalJobDefinition, LocalJobSchedule, default_local_jobs
from binance_spot_bot.local_scheduler import due_jobs, scheduler_tick
from binance_spot_bot.operator_runbooks import default_runbooks, export_runbooks, validate_runbook_commands
from binance_spot_bot.paper_ops_calendar import export_paper_ops_calendar, paper_ops_calendar
from binance_spot_bot.runbook_drills import run_runbook_drill, write_runbook_drill
from binance_spot_bot.scheduled_reports import scheduled_report_plan, write_scheduled_report
from binance_spot_bot.windows_task_scheduler import windows_task_plan, write_windows_scheduler_scripts


def test_local_job_schema_store_and_secret_free_outputs(tmp_path):
    store = LocalJobStore(tmp_path / "local-jobs")
    jobs = default_local_jobs()
    path = store.save_jobs(jobs)
    loaded = store.load_jobs()

    assert path.exists()
    assert loaded[0].job_id == jobs[0].job_id
    assert all(job.live_trading_enabled is False for job in loaded)
    assert "SECRET" not in path.read_text(encoding="utf-8")


def test_allowlist_blocks_live_order_account_shell_and_secret_args():
    assert is_safe_command("operator-report --json") is True
    assert is_safe_command("weekly-governance-report --json") is True
    assert validate_local_job_command("demo-execution-place --armed").allowed is False
    assert validate_local_job_command("paper-session --mode live").allowed is False
    assert validate_local_job_command("operator-report --json; whoami").allowed is False
    assert validate_local_job_command("operator-report --api-key placeholder").allowed is False


def test_runner_validates_executes_safe_job_and_redacts_env(tmp_path, monkeypatch):
    monkeypatch.setenv("BINANCE_API_SECRET", "SHOULD_NOT_LEAK")
    ready = run_local_job("operator-health-score --json")
    blocked = run_local_job("withdraw funds")
    result = run_local_job(
        LocalJobDefinition("smoke", "Smoke", "Run redaction self-test", "redaction-self-test", ["--json"], max_runtime_seconds=30),
        root=tmp_path,
        execute=True,
    )

    assert ready["status"] == "ready"
    assert blocked["status"] == "blocked"
    assert result["status"] == "ok"
    assert "SHOULD_NOT_LEAK" not in json.dumps(result)


def test_scheduler_due_jobs_dry_run_and_lock(tmp_path):
    due = LocalJobDefinition(
        "due",
        "Due",
        "Due job",
        "operator-health-score",
        ["--json"],
        LocalJobSchedule("interval", {"next_due_ms": 1}),
    )
    future = LocalJobDefinition(
        "future",
        "Future",
        "Future job",
        "operator-report",
        ["--json"],
        LocalJobSchedule("interval", {"next_due_ms": 9999999999999}),
    )
    store = LocalJobStore(tmp_path / "local-jobs")
    store.save_jobs([due, future])
    tick = scheduler_tick(tmp_path, dry_run=True, now_ms=10)

    assert due_jobs([{"job_id": "a", "next_due_ms": 1}], 2)["jobs"][0]["job_id"] == "a"
    assert tick["status"] == "dry_run"
    assert tick["due"] == ["due"]


def test_scheduled_reports_runbooks_reminders_calendar_and_drills(tmp_path):
    plan = scheduled_report_plan()
    report_path = write_scheduled_report(tmp_path, "daily", plan)
    runbooks = default_runbooks()
    runbook_paths = export_runbooks(tmp_path)
    reminders = governance_reminders(root=tmp_path)
    reminders_path = write_governance_reminders(tmp_path, reminders)
    calendar = paper_ops_calendar(plan["jobs"])
    calendar_paths = export_paper_ops_calendar(tmp_path, calendar)
    drill = run_runbook_drill("failed_scheduled_report")
    drill_path = write_runbook_drill(tmp_path, drill)

    assert report_path.exists()
    assert all(validate_runbook_commands(book)["status"] == "ok" for book in runbooks)
    assert runbook_paths["json"]
    assert reminders_path.exists()
    assert reminders["live_trading_enabled"] is False
    assert calendar_paths["ics"].endswith(".ics")
    assert drill["status"] == "passed"
    assert drill_path.exists()


def test_windows_scheduler_plan_is_confirmed_safe_and_path_space_aware(tmp_path):
    repo = tmp_path / "Repo With Spaces"
    repo.mkdir()
    blocked = windows_task_plan("demo-execution-place --armed", repo_root=repo)
    allowed = windows_task_plan("local-scheduler-tick --dry-run --json", repo_root=repo)
    scripts = write_windows_scheduler_scripts(tmp_path, repo, confirm="INSTALL_LOCAL_OPS")

    assert blocked["status"] == "blocked"
    assert allowed["allowed"] is True
    assert str(repo) in allowed["command_line"]
    assert "run-local-ops-tick.ps1" in scripts
    script_text = (tmp_path / "scripts" / "run-local-ops-tick.ps1").read_text(encoding="utf-8")
    assert "LIVE_TRADING_ENABLED" in script_text
    assert "BINANCE_API_SECRET" not in script_text

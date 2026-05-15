from pathlib import Path

import pytest

from binance_spot_bot.cli_profiler import SAFE_ENV, profile_cli_command
from binance_spot_bot.dashboard_profiler import DashboardProfiler, profile_dashboard_panels
from binance_spot_bot.data_performance import analyze_data_performance
from binance_spot_bot.io_profiler import profile_json_write
from binance_spot_bot.performance_budget import evaluate_performance_budget, load_performance_budgets, performance_budget
from binance_spot_bot.performance_evidence_bundle import export_performance_evidence_bundle, verify_performance_evidence_bundle
from binance_spot_bot.performance_recommendations import performance_recommendations
from binance_spot_bot.performance_regression import detect_performance_regression
from binance_spot_bot.performance_store import save_profile_run, verify_performance_manifest
from binance_spot_bot.profiling_core import ProfileRun, profile_block, summarize_profile_run, write_profile_run
from binance_spot_bot.resource_monitor import resource_snapshot
from binance_spot_bot.runtime_profiler import profile_runtime_steps, runtime_profile


def test_profile_core_spans_exceptions_and_store(tmp_path: Path):
    run = ProfileRun("unit-profile", "test")
    with profile_block("ok-span", "test", {"api_secret": "hidden"}, run):
        pass
    with pytest.raises(RuntimeError):
        with profile_block("bad-span", "test", {}, run):
            raise RuntimeError("boom")
    summary = summarize_profile_run(run)
    assert summary["span_count"] == 2
    assert run.to_dict()["live_trading_enabled"] is False
    paths = write_profile_run(run, tmp_path)
    assert Path(paths["path"]).exists()
    manifest = save_profile_run(tmp_path, run.to_dict())
    assert verify_performance_manifest(manifest["manifest"])["status"] == "ok"


def test_runtime_cli_dashboard_resource_io_and_data_profiles(tmp_path: Path):
    runtime = profile_runtime_steps(steps=["data_source.next_event", "risk_decision"])
    assert runtime["summary"]["span_count"] == 2
    cli = profile_cli_command(tmp_path, "python -m binance_spot_bot.cli diagnostics", execute=False)
    assert cli["safe_env"] == SAFE_ENV
    dashboard = profile_dashboard_panels(["overview", "performance"])
    assert dashboard["summary"]["span_count"] == 2
    profiler = DashboardProfiler(enabled=False)
    with profiler.measure("disabled"):
        pass
    assert profiler.summary()["span_count"] == 0
    resources = resource_snapshot(tmp_path, tracemalloc_enabled=True)
    assert resources["live_trading_enabled"] is False
    io = profile_json_write(tmp_path / "data" / "x.json", {"status": "ok"})
    assert io["status"] == "ready"
    data = analyze_data_performance(tmp_path)
    assert data["status"] == "ready"


def test_budgets_regressions_recommendations_and_evidence(tmp_path: Path):
    assert load_performance_budgets()["status"] == "ready"
    assert evaluate_performance_budget("cli_command_ms", 1)["status"] == "ok"
    assert evaluate_performance_budget("cli_command_ms", 7000)["status"] in {"warn", "fail"}
    legacy = performance_budget(30, 20)
    assert legacy["status"] == "warn"
    regression = detect_performance_regression("duration_ms", 100, 140)
    assert regression["status"] == "regression"
    recommendations = performance_recommendations({"status": "regression", "slowest_spans": [{"name": "panel", "category": "dashboard", "duration_ms": 1200}]})
    assert recommendations["recommendations"]
    source = tmp_path / "perf.json"
    source.write_text('{"status":"ready","live_trading_enabled":false}', encoding="utf-8")
    bundle = export_performance_evidence_bundle([source], tmp_path / "evidence")
    assert verify_performance_evidence_bundle(bundle["manifest"])["status"] == "ok"


def test_legacy_runtime_profile():
    assert runtime_profile(10)["status"] == "ok"
    assert runtime_profile(2000)["status"] == "warn"

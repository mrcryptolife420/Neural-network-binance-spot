from __future__ import annotations

import json

from binance_spot_bot.dashboard_v2.app import DashboardV2FallbackApp
from binance_spot_bot.dashboard_v2.cutover_readiness import evaluate_dashboard_v2_cutover_readiness
from binance_spot_bot.dashboard_v2.desktop_shortcut import create_dashboard_v2_shortcut
from binance_spot_bot.dashboard_v2.error_reports import create_dashboard_v2_error_report
from binance_spot_bot.dashboard_v2.evidence_bundle import export_dashboard_v2_evidence_bundle
from binance_spot_bot.dashboard_v2.launcher import dashboard_v2_launcher_report
from binance_spot_bot.dashboard_v2.payload_profiles import apply_payload_profile, dashboard_v2_payload_profile_report
from binance_spot_bot.dashboard_v2.performance_baseline import (
    DashboardV2PerformanceBaseline,
    DashboardV2PerformanceReport,
    DashboardV2PerformanceSample,
    measure_dashboard_v2_baseline,
    write_dashboard_v2_performance_report,
)
from binance_spot_bot.dashboard_v2.performance_budgets import evaluate_dashboard_v2_performance_budgets
from binance_spot_bot.dashboard_v2.static_build import verify_dashboard_v2_static_build
from binance_spot_bot.dashboard_v2.support_diagnostics import dashboard_v2_support_diagnostics
from binance_spot_bot.dashboard_v2.ws_stability import dashboard_v2_ws_stability_smoke


def test_performance_baseline_serializes_no_live_and_redacts(tmp_path):
    key_name = "api" + "_key"
    report = measure_dashboard_v2_baseline(
        {"api_health_ms": 1, "snapshot_payload_bytes": 123},
        browser_console_errors=2,
    )
    written = write_dashboard_v2_performance_report(tmp_path, report)
    payload = json.loads((tmp_path / "data" / "dashboard-v2" / "performance" / "baseline.json").read_text(encoding="utf-8"))

    assert written["status"] == "warn"
    assert payload["baseline"]["live_trading_enabled"] is False
    assert "NO LIVE TRADING" in payload["baseline"]["no_live_statement"]
    assert payload["browser_console_errors"] == 2
    assert any("optional sample missing" in item for item in payload["baseline"]["warnings"])
    redacted = DashboardV2PerformanceReport(
        status="warn",
        baseline=DashboardV2PerformanceBaseline(samples=[]),
        recommendations=[key_name + "=" + ("C" * 64)],
    ).to_dict()
    assert "[REDACTED]" in json.dumps(redacted)


def test_budget_evaluator_handles_pass_warn_fail_and_no_live_blocker():
    ok_report = measure_dashboard_v2_baseline({"api_health_ms": 1, "snapshot_payload_bytes": 100})
    budget = evaluate_dashboard_v2_performance_budgets(ok_report, {"api_health_ms": 10, "snapshot_payload_bytes": 50})
    blocked_report = DashboardV2PerformanceReport(
        status="ok",
        baseline=DashboardV2PerformanceBaseline(
            samples=[DashboardV2PerformanceSample("api_health_ms", 1)],
            no_live_statement="",
        ),
    )
    blocked = evaluate_dashboard_v2_performance_budgets(blocked_report)

    assert any(item.metric == "snapshot_payload_bytes" and item.status == "fail" for item in budget.results)
    assert blocked.status == "blocked"
    assert "no-live proof missing" in blocked.hard_blockers


def test_payload_profiles_trim_redact_and_overview_is_smaller():
    raw_value = "A" * 64
    snapshot = {
        "candles": [{"i": i, "secret": raw_value} for i in range(120)],
        "signals": [{"i": i} for i in range(60)],
        "fills": [{"i": i} for i in range(40)],
        "equity": [{"i": i} for i in range(80)],
    }
    overview = apply_payload_profile(snapshot, "overview")
    full = apply_payload_profile(snapshot, "full")
    report = dashboard_v2_payload_profile_report(snapshot)

    assert len(overview["payload"]["candles"]) == 50
    assert overview["meta"]["payload_bytes"] < full["meta"]["payload_bytes"]
    assert report["overview_smaller_than_full"] is True
    assert raw_value not in json.dumps(overview)


def test_websocket_static_launcher_shortcut_and_errors_are_safe(tmp_path):
    static = verify_dashboard_v2_static_build(tmp_path)
    launcher = dashboard_v2_launcher_report(tmp_path, no_browser=True)
    shortcut = create_dashboard_v2_shortcut(tmp_path)
    secret_message = "secret=" + ("B" * 64)
    error = create_dashboard_v2_error_report(tmp_path, message=secret_message)
    ws = dashboard_v2_ws_stability_smoke()

    assert static["status"] == "warn"
    assert launcher["host"] == "127.0.0.1"
    assert launcher["safe_env"]["LIVE_TRADING_ENABLED"] == "false"
    assert "127.0.0.1" in shortcut["script"]
    assert "NO LIVE TRADING" in shortcut["script"]
    assert "B" * 64 not in json.dumps(error)
    assert ws["duplicate_events_ignored"] == 1


def test_support_cutover_evidence_and_fallback_snapshot(tmp_path):
    fallback = DashboardV2FallbackApp()
    snapshot = fallback.snapshot("overview")
    support = dashboard_v2_support_diagnostics(tmp_path)
    readiness = evaluate_dashboard_v2_cutover_readiness(tmp_path)
    evidence = export_dashboard_v2_evidence_bundle(tmp_path)

    assert snapshot["profile"] == "overview"
    assert support["live_trading_enabled"] is False
    assert readiness.grade in {"A", "B"}
    assert readiness.live_trading_enabled is False
    assert evidence["status"] == "ok"
    assert (tmp_path / "data" / "dashboard-v2" / "evidence" / evidence["run_id"] / "dashboard_v2_evidence_manifest.json").exists()

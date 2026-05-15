from __future__ import annotations

import json

from binance_spot_bot.dashboard_v2.dependency_isolation import dashboard_v2_dependency_isolation
from binance_spot_bot.dashboard_v2.legacy_archive import create_dashboard_v2_legacy_archive, verify_dashboard_v2_legacy_archive
from binance_spot_bot.dashboard_v2.release_hardening import (
    dashboard_v2_check_all_profile,
    dashboard_v2_component_cleanup_report,
    dashboard_v2_docs_v2_only_lock,
    dashboard_v2_legacy_test_cleanup_report,
    dashboard_v2_post_removal_verify,
    dashboard_v2_release_simulation,
    dashboard_v2_removal_patch_plan,
    dashboard_v2_removal_rollback_drill,
    dashboard_v2_runtime_state_coupling_audit,
    dashboard_v2_streamlit_isolation_plan,
    dashboard_v2_streamlit_removal_execute,
    dashboard_v2_support_evidence_smoke,
    export_dashboard_v2_only_release_evidence,
)
from binance_spot_bot.dashboard_v2.removal_readiness_gate import (
    StreamlitRemovalGateInput,
    evaluate_streamlit_removal_readiness,
    write_streamlit_removal_readiness_report,
)


def test_removal_gate_outcomes_and_safety(tmp_path):
    remove_now = evaluate_streamlit_removal_readiness(tmp_path, StreamlitRemovalGateInput(rollback_archive_present=True))
    blocked = evaluate_streamlit_removal_readiness(tmp_path, StreamlitRemovalGateInput())
    keep = evaluate_streamlit_removal_readiness(tmp_path, StreamlitRemovalGateInput(deprecation_gate="blocked", rollback_archive_present=True))
    unsafe = evaluate_streamlit_removal_readiness(tmp_path, StreamlitRemovalGateInput(rollback_archive_present=True, live_mode_found=True))

    assert remove_now.decision.outcome == "remove_now"
    assert remove_now.decision.remove_code_now is False
    assert blocked.decision.outcome == "blocked_cleanup_required"
    assert keep.decision.outcome == "keep_legacy"
    assert unsafe.decision.outcome == "unsafe"
    assert "NO LIVE TRADING" in remove_now.no_live_statement


def test_dependency_archive_and_rollback_drill(tmp_path):
    (tmp_path / "src" / "binance_spot_bot" / "ui").mkdir(parents=True)
    (tmp_path / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").write_text("NO LIVE TRADING\n", encoding="utf-8")
    (tmp_path / "src" / "binance_spot_bot" / "ui" / "components.py").write_text("", encoding="utf-8")
    (tmp_path / "src" / "binance_spot_bot" / "ui" / "page_registry.py").write_text("", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project.optional-dependencies]\ndashboard-v2=[]\nlegacy-streamlit=[]\n", encoding="utf-8")

    isolation = dashboard_v2_dependency_isolation(tmp_path)
    archive = create_dashboard_v2_legacy_archive(tmp_path)
    verify = verify_dashboard_v2_legacy_archive(archive["manifest"])
    drill = dashboard_v2_removal_rollback_drill(tmp_path)

    assert isolation["status"] == "ok"
    assert archive["status"] == "ok"
    assert verify["status"] == "ok"
    assert drill["status"] == "ok"
    assert drill["mutates_worktree"] is False


def test_release_hardening_reports_and_execution_guard(tmp_path):
    reports = [
        dashboard_v2_streamlit_isolation_plan(tmp_path),
        dashboard_v2_component_cleanup_report(tmp_path),
        dashboard_v2_check_all_profile("v2-only"),
        dashboard_v2_support_evidence_smoke(tmp_path),
        dashboard_v2_release_simulation(tmp_path),
        dashboard_v2_docs_v2_only_lock(),
        dashboard_v2_legacy_test_cleanup_report(),
        dashboard_v2_runtime_state_coupling_audit(tmp_path),
        dashboard_v2_removal_patch_plan(tmp_path),
        dashboard_v2_post_removal_verify(tmp_path),
    ]
    dry_run = dashboard_v2_streamlit_removal_execute(tmp_path, dry_run=True)
    blocked = dashboard_v2_streamlit_removal_execute(tmp_path, dry_run=False, confirm="")

    assert all(report["live_trading_enabled"] is False for report in reports)
    assert dry_run["status"] == "dry_run"
    assert blocked["status"] == "blocked"


def test_v2_only_release_evidence_and_readiness_report_are_secret_free(tmp_path):
    written = write_streamlit_removal_readiness_report(tmp_path)
    evidence = export_dashboard_v2_only_release_evidence(tmp_path)
    text = json.dumps(evidence) + json.dumps(written)

    assert written["live_trading_enabled"] is False
    assert evidence["status"] == "ok"
    assert "dashboard_v2_only_release_evidence_manifest.json" in evidence["manifest"]
    assert "api_key" not in text.lower()
    assert (tmp_path / "data" / "dashboard-v2" / "v2-only-release" / "evidence" / evidence["run_id"] / "dashboard_v2_only_release_evidence_manifest.json").exists()

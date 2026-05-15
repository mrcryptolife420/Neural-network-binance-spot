from __future__ import annotations

import json

from binance_spot_bot.dashboard_v2.actionable_issues import dashboard_v2_actionable_issues
from binance_spot_bot.dashboard_v2.command_palette import dashboard_v2_command_palette_smoke
from binance_spot_bot.dashboard_v2.demo_spot_flow import dashboard_v2_demo_spot_flow_smoke
from binance_spot_bot.dashboard_v2.guided_actions import dashboard_v2_guided_actions
from binance_spot_bot.dashboard_v2.navigation_map import dashboard_v2_navigation_map
from binance_spot_bot.dashboard_v2.onboarding import dashboard_v2_onboarding_report
from binance_spot_bot.dashboard_v2.operator_journey_map import dashboard_v2_operator_journey_map
from binance_spot_bot.dashboard_v2.paper_session_flow import dashboard_v2_paper_session_flow_smoke
from binance_spot_bot.dashboard_v2.start_wizard import dashboard_v2_start_wizard_smoke
from binance_spot_bot.dashboard_v2.status_language import dashboard_v2_status_language_report
from binance_spot_bot.dashboard_v2.streamlit_deprecation_readiness import (
    dashboard_v2_streamlit_deprecation_readiness,
    dashboard_v2_streamlit_fallback_info,
)
from binance_spot_bot.dashboard_v2.uat_feedback_execution import dashboard_v2_uat_feedback_execution
from binance_spot_bot.dashboard_v2.ux_backlog_ingest import (
    DashboardV2UxFinding,
    ingest_dashboard_v2_ux_backlog,
    write_dashboard_v2_ux_backlog,
)
from binance_spot_bot.dashboard_v2.ux_metrics import dashboard_v2_ux_metrics
from binance_spot_bot.dashboard_v2.workflow_evidence_bundle import export_dashboard_v2_workflow_evidence_bundle


def test_ux_backlog_ingest_prioritizes_groups_and_redacts(tmp_path):
    secret = "D" * 64
    report = ingest_dashboard_v2_ux_backlog(
        tmp_path,
        [
            DashboardV2UxFinding("manual", "no-live confusion " + secret, "no_live_safety", "warning"),
            DashboardV2UxFinding("uat", "critical workflow blocked", "runtime_controls", "blocked"),
            DashboardV2UxFinding("browser", "critical workflow blocked", "runtime_controls", "blocked"),
        ],
    ).to_dict()
    written = write_dashboard_v2_ux_backlog(tmp_path)

    priorities = {item["title"]: item["priority"] for item in report["backlog"]["items"]}
    grouped = [item for item in report["backlog"]["items"] if item["title"] == "critical workflow blocked"][0]
    assert priorities["no-live confusion [REDACTED]"] == "UX-P0"
    assert grouped["count"] == 2
    assert secret not in json.dumps(report)
    assert written["live_trading_enabled"] is False


def test_journeys_guided_actions_wizards_and_flows_are_no_live():
    journey = dashboard_v2_operator_journey_map()
    actions = dashboard_v2_guided_actions()
    start = dashboard_v2_start_wizard_smoke("demo")
    live_blocked = dashboard_v2_start_wizard_smoke("live")
    demo = dashboard_v2_demo_spot_flow_smoke(profile_ok=False)
    paper = dashboard_v2_paper_session_flow_smoke()

    assert all(any(step["no_live_step"] for step in item["steps"]) for item in journey["journeys"])
    assert all(action["live_trading_enabled"] is False for action in actions["actions"])
    assert start["status"] == "ok"
    assert live_blocked["status"] == "blocked"
    assert demo["status"] == "blocked"
    assert paper["stop_always_visible"] is True


def test_navigation_palette_status_onboarding_metrics_and_uat_are_safe(tmp_path):
    issues = dashboard_v2_actionable_issues()
    navigation = dashboard_v2_navigation_map()
    palette = dashboard_v2_command_palette_smoke()
    status = dashboard_v2_status_language_report()
    onboarding = dashboard_v2_onboarding_report(tmp_path)
    metrics = dashboard_v2_ux_metrics([{"type": "page_load"}, {"type": "no_live_view"}, {"type": "action_start", "status": "blocked"}])
    uat_blocked = dashboard_v2_uat_feedback_execution([{"id": "1", "priority": "UX-P0", "status": "deferred"}])

    assert issues["top_priority"] == "no_live_safety"
    assert navigation["orphaned_pages"] == []
    assert palette["status"] == "ok"
    assert status["forbidden_phrases"] == []
    assert onboarding["works_without_api_keys"] is True
    assert metrics["aggregate"]["blocked_action_count"] == 1
    assert uat_blocked["status"] == "blocked"


def test_streamlit_fallback_deprecation_and_workflow_evidence(tmp_path):
    fallback = dashboard_v2_streamlit_fallback_info()
    deprecation = dashboard_v2_streamlit_deprecation_readiness(tmp_path)
    evidence = export_dashboard_v2_workflow_evidence_bundle(tmp_path)

    assert fallback["fallback_available"] is True
    assert deprecation["streamlit_removed"] is False
    assert deprecation["grade"] == "deprecation_candidate"
    assert evidence["status"] == "ok"
    assert (tmp_path / "data" / "dashboard-v2" / "workflow-evidence" / evidence["run_id"] / "dashboard_v2_workflow_evidence_manifest.json").exists()

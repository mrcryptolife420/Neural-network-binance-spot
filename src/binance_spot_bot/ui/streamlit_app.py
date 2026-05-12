from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict, replace
from decimal import Decimal
from pathlib import Path

import streamlit as st

from binance_spot_bot.binance import BinanceSpotAdapter
from binance_spot_bot.config import BotSettings
from binance_spot_bot.connectivity import connectivity_report
from binance_spot_bot.credentials import CredentialManager, WindowsSecretStoreAdapter
from binance_spot_bot.chaos import simulate_failure
from binance_spot_bot.copilot_permissions import check_copilot_action
from binance_spot_bot.demo_execution_sandbox import DemoExecutionSandbox, intent_from_values
from binance_spot_bot.demo_pilot import operator_checklist, pilot_presets, pipeline_rows
from binance_spot_bot.cache_manager import cache_manifest
from binance_spot_bot.dashboard_state import DashboardProcessStatus, DashboardRuntimeState, bot_status_from_runtime
from binance_spot_bot.dashboard_evidence import build_operator_evidence, write_operator_evidence
from binance_spot_bot.demo_acceptance_rehearsal import DemoAcceptanceRehearsal, RehearsalHistory
from binance_spot_bot.diagnostics import collect_diagnostics
from binance_spot_bot.evidence import EvidenceVault
from binance_spot_bot.evidence_scorecard import generate_evidence_scorecard, write_scorecard
from binance_spot_bot.evaluation import evaluate_rule_baseline, evaluate_walk_forward, report_to_dict
from binance_spot_bot.experiment_db import ExperimentDB
from binance_spot_bot.governance_simulation import run_governance_simulation
from binance_spot_bot.local_ops_automation import generate_scheduled_ops_report
from binance_spot_bot.metrics_warehouse import write_metrics_report
from binance_spot_bot.ops_assistant import answer_ops_question
from binance_spot_bot.action_center import create_reviewed_action
from binance_spot_bot.action_proposals import ActionSafetyClass, proposal_from_command
from binance_spot_bot.approval_queue import ApprovalQueueStore
from binance_spot_bot.approval_workflow import ApprovalWorkflow
from binance_spot_bot.decision_journal import DecisionJournal
from binance_spot_bot.permission_profiles import permission_compliance_report
from binance_spot_bot.compliance_report import write_compliance_report
from binance_spot_bot.permission_drift import permission_drift
from binance_spot_bot.local_operator_identity import local_operator_identity
from binance_spot_bot.backup_profiles import backup_profiles
from binance_spot_bot.state_integrity import state_integrity_check
from binance_spot_bot.disaster_recovery_drills import run_disaster_recovery_drill
from binance_spot_bot.versioning import version_payload
from binance_spot_bot.roadmap_index import build_roadmap_index
from binance_spot_bot.repo_inventory import repo_inventory
from binance_spot_bot.intelligent_test_selector import selected_tests
from binance_spot_bot.performance_budget import performance_budget
from binance_spot_bot.runtime_snapshot_builder import build_runtime_snapshot
from binance_spot_bot.data_quality_v2 import data_quality_v2
from binance_spot_bot.training_pipeline import run_training_pipeline
from binance_spot_bot.model_health_score import model_health_score
from binance_spot_bot.ensemble_prediction import ensemble_prediction
from binance_spot_bot.paper_os_simulation import paper_os_simulation
from binance_spot_bot.stabilization_gate import stabilization_gate
from binance_spot_bot.operator_glossary import operator_glossary
from binance_spot_bot.exchange_profiles import BINANCE_DEMO_SPOT_PROFILE, available_profiles, selectable_profile_names
from binance_spot_bot.html_reports import export_html_report
from binance_spot_bot.indicator_warmup import warmup_indicators
from binance_spot_bot.indicators import (
    INDICATOR_PROFILES,
    allocation_hints,
    indicator_rows_from_runtimes,
    indicator_summary,
    write_indicator_evidence,
)
from binance_spot_bot.manual_demo_trading import ManualDemoTradeRequest, execute_manual_demo_trade
from binance_spot_bot.model_registry import ModelRegistry
from binance_spot_bot.multi_symbol import (
    DEFAULT_DEMO_SYMBOLS,
    allocation_plan,
    choose_active_symbols,
    next_multi_action,
    risk_limit_rows,
    summarize_multi_rows,
    validate_demo_symbols,
    write_multi_symbol_evidence,
)
from binance_spot_bot.notebook_export import export_notebook
from binance_spot_bot.operator_ops import (
    artifact_catalog,
    data_growth_budget,
    diagnostics_baseline,
    environment_doctor,
    evidence_chain,
    export_operator_report,
    incident_timeline,
    local_ops_snapshot,
    operator_command_manifest,
    operator_health_score,
    operator_report_diff,
    redaction_self_test,
    rehearsal_profiles,
    report_index,
    retention_preview,
    verify_support_bundles,
)
from binance_spot_bot.pilot_runner import PilotRunnerService, start_background_runner
from binance_spot_bot.portfolio import Portfolio, Position
from binance_spot_bot.preflight import run_preflight
from binance_spot_bot.readiness import score_readiness
from binance_spot_bot.replay_sandbox import ReplaySandbox
from binance_spot_bot.risk_debugger import explain_decision, timeline_from_events
from binance_spot_bot.scanner_history import ScannerHistory, ScannerRow, rank_watchlist
from binance_spot_bot.session_compare import compare_sessions
from binance_spot_bot.signal_explainer import explain_signal
from binance_spot_bot.settings_store import DashboardSettingsStore, RISK_PRESETS
from binance_spot_bot.session_store import SessionStore
from binance_spot_bot.spot_preview import SpotPreview, load_spot_symbol_preview
from binance_spot_bot.strategy_templates import list_strategy_templates
from binance_spot_bot.support_bundle import create_support_bundle
from binance_spot_bot.testnet_endurance import TestnetEnduranceGuard
from binance_spot_bot.types import FeatureRow, OrderSide
from binance_spot_bot.ui.chart_registry import (
    DEMO_PILOT_COMMAND_STATUS,
    DEMO_PILOT_COUNTERS,
    DEMO_PILOT_EQUITY_PNL,
    DEMO_PILOT_HEARTBEAT,
    OVERVIEW_CANDLESTICK,
    OVERVIEW_EQUITY,
)
from binance_spot_bot.ui.charts import (
    candlestick_figure,
    command_status_figure,
    equity_figure,
    multi_symbol_overview_figure,
    runner_counters_figure,
    runner_equity_pnl_figure,
    runner_heartbeat_figure,
)
from binance_spot_bot.ui.components import render_alert_list, render_badges, render_debug, render_plotly_chart, render_table
from binance_spot_bot.ui.demo_trading import demo_trading_badge
from binance_spot_bot.ui.page_registry import page_titles, validate_page_registry
from binance_spot_bot.ui.state import SELECTABLE_DATA_SOURCES, SELECTABLE_MODES, create_runtime
from binance_spot_bot.ui.wizard import wizard_options
from binance_spot_bot.workspaces import WorkspaceProfile, WorkspaceStore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--mode", choices=SELECTABLE_MODES, default="demo")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--interval", default="1m")
    parser.add_argument("--scenario", default="sideways")
    parser.add_argument("--source", choices=SELECTABLE_DATA_SOURCES, default="auto")
    args, _ = parser.parse_known_args(sys.argv[1:])
    return args


def main() -> None:
    args = parse_args()
    validate_page_registry()
    st.set_page_config(page_title="Spot Bot Control Center", layout="wide")
    st.title("Neural Network Binance Spot Bot")
    st.caption("LIVE TRADING DISABLED")
    st.caption("Advanced tools: Overview, Demo Spot Trading, Demo Pilot.")

    base_settings = BotSettings.from_env()
    store = DashboardSettingsStore(base_settings.data_dir / "settings")
    if "dashboard_settings" not in st.session_state:
        st.session_state.dashboard_settings = store.load()
    if "credential_manager" not in st.session_state:
        st.session_state.credential_manager = CredentialManager()
    if "connectivity_report" not in st.session_state:
        st.session_state.connectivity_report = {}
    if "evaluation_report" not in st.session_state:
        st.session_state.evaluation_report = {}
    if "manual_demo_fills" not in st.session_state:
        st.session_state.manual_demo_fills = []
    if "demo_trading_armed" not in st.session_state:
        st.session_state.demo_trading_armed = False
    if "demo_pilot_preset" not in st.session_state:
        st.session_state.demo_pilot_preset = "smoke"
    if "multi_demo_runtimes" not in st.session_state:
        st.session_state.multi_demo_runtimes = {}
    if "multi_demo_running" not in st.session_state:
        st.session_state.multi_demo_running = False
    if "multi_demo_cycles" not in st.session_state:
        st.session_state.multi_demo_cycles = {}

    saved = st.session_state.dashboard_settings
    profiles = available_profiles()

    with st.sidebar:
        st.header("Dashboard")
        dashboard_view = st.radio("View", ["Simple demo trading", "Advanced tools"], horizontal=False)
        simple_dashboard = dashboard_view == "Simple demo trading"
        selected_profile = st.selectbox(
            "Exchange profile",
            selectable_profile_names(),
            index=selectable_profile_names().index(saved.selected_profile)
            if saved.selected_profile in selectable_profile_names()
            else 0,
            format_func=lambda value: profiles[value].label,
        )
        symbol = st.text_input("Symbol", value=saved.symbol or args.symbol).upper()
        intervals = ["1m", "5m", "15m", "1h"]
        if simple_dashboard:
            mode = "demo"
            source = saved.source if saved.source in SELECTABLE_DATA_SOURCES else "auto"
            interval = saved.interval if saved.interval in intervals else "1m"
            scenario = saved.scenario or "sideways"
            model_alias = saved.model_alias
            speed = 5
            st.header("Demo bot")
            reset_runtime = st.button("Reset demo bot", use_container_width=True)
            start = False
            pause = False
            step_once = False
            emergency_stop = st.button("Stop demo bot", use_container_width=True)
            st.session_state.demo_pilot_preset = "smoke"
            if st.button("Connect demo trading", use_container_width=True):
                st.session_state.demo_trading_armed = selected_profile == BINANCE_DEMO_SPOT_PROFILE
            if st.button("Disconnect demo trading", use_container_width=True):
                st.session_state.demo_trading_armed = False
            st.caption("Advanced tools blijven beschikbaar via de view-keuze hierboven.")
        else:
            st.header("Control")
            mode = st.selectbox("Runtime mode", SELECTABLE_MODES, index=SELECTABLE_MODES.index(args.mode))
            source = st.selectbox(
                "Market data source",
                SELECTABLE_DATA_SOURCES,
                index=SELECTABLE_DATA_SOURCES.index(saved.source if saved.source in SELECTABLE_DATA_SOURCES else args.source),
            )
            interval = st.selectbox(
                "Interval",
                intervals,
                index=intervals.index(saved.interval if saved.interval in intervals else args.interval),
            )
            scenario = st.selectbox("Demo scenario", ["sideways", "uptrend", "downtrend", "volatile"], index=0)
            model_alias = st.text_input("Model alias", value=saved.model_alias)
            speed = st.selectbox("Replay speed", [1, 5, 10], index=0)
            st.header("Run")
            reset_runtime = st.button("Reset runtime", use_container_width=True)
            start = st.button("Start / run", use_container_width=True)
            pause = st.button("Pause", use_container_width=True)
            step_once = st.button("Single step", use_container_width=True)
            emergency_stop = st.button("Emergency stop", use_container_width=True)
            st.header("Demo Spot")
            st.session_state.demo_pilot_preset = st.selectbox(
                "Pilot mode",
                list(pilot_presets().keys()),
                index=list(pilot_presets().keys()).index(st.session_state.demo_pilot_preset)
                if st.session_state.demo_pilot_preset in pilot_presets()
                else 0,
            )
            if st.button("Arm demo trading", use_container_width=True):
                st.session_state.demo_trading_armed = selected_profile == BINANCE_DEMO_SPOT_PROFILE
            if st.button("Disarm demo trading", use_container_width=True):
                st.session_state.demo_trading_armed = False

    profile = profiles[selected_profile]
    st.session_state.credential_manager.set_session_credentials(
        selected_profile,
        st.session_state.credential_manager._api_key,
        st.session_state.credential_manager._api_secret,
    )
    runtime_settings = st.session_state.credential_manager.apply_to_settings(base_settings, selected_profile)

    current_preset = RISK_PRESETS.get(saved.risk_preset, RISK_PRESETS["balanced"])
    tabs = None
    if not simple_dashboard:
        tabs = st.tabs(page_titles())
        with tabs[4]:
            st.subheader("Risk controls")
            with st.form("risk_controls"):
                risk_preset = st.selectbox("Risk preset", list(RISK_PRESETS.keys()), index=list(RISK_PRESETS.keys()).index(saved.risk_preset if saved.risk_preset in RISK_PRESETS else "balanced"))
                preset = RISK_PRESETS[risk_preset]
                max_daily_loss = Decimal(str(st.number_input("Max daily loss quote", value=float(preset["max_daily_loss_quote"]), min_value=0.0)))
                max_position = Decimal(str(st.number_input("Max position quote", value=float(preset["max_position_quote"]), min_value=0.0)))
                max_trades = st.number_input("Max trades per day", value=int(preset["max_trades_per_day"]), min_value=0, step=1)
                min_conf = st.slider("Min signal confidence", 0.0, 1.0, float(preset["min_signal_confidence"]), 0.01)
                max_spread = Decimal(str(st.number_input("Max spread bps", value=float(preset["max_spread_bps"]), min_value=0.0)))
                max_data_age_ms = st.number_input("Max data age ms", value=int(preset["max_data_age_ms"]), min_value=1_000, step=1_000)
                default_quote_size = Decimal(str(st.number_input("Default quote size", value=float(preset["default_quote_size"]), min_value=0.0)))
                apply_risk = st.form_submit_button("Apply risk settings")
            if apply_risk:
                saved.risk_preset = risk_preset
                store.save(saved)
                st.success("Risk settings applied to next runtime reset.")
    if "max_daily_loss" not in locals():
        max_daily_loss = Decimal(str(current_preset["max_daily_loss_quote"]))
        max_position = Decimal(str(current_preset["max_position_quote"]))
        max_trades = int(current_preset["max_trades_per_day"])
        min_conf = float(current_preset["min_signal_confidence"])
        max_spread = Decimal(str(current_preset["max_spread_bps"]))
        max_data_age_ms = int(current_preset["max_data_age_ms"])
        default_quote_size = Decimal(str(current_preset["default_quote_size"]))

    runtime_key = (
        selected_profile,
        mode,
        source,
        symbol,
        interval,
        scenario,
        model_alias,
        str(max_daily_loss),
        str(max_position),
        int(max_trades),
        float(min_conf),
        str(max_spread),
        int(max_data_age_ms),
        str(default_quote_size),
        st.session_state.credential_manager.status().api_key_fingerprint,
        bool(st.session_state.demo_trading_armed),
        st.session_state.demo_pilot_preset,
    )
    if reset_runtime or st.session_state.get("runtime_key") != runtime_key:
        st.session_state.runtime = create_runtime(
            runtime_settings,
            mode,
            symbol,
            interval,
            scenario,
            7,
            max_daily_loss,
            max_position,
            int(max_trades),
            float(min_conf),
            max_spread,
            source,
            model_alias,
            int(max_data_age_ms),
            default_quote_size,
            bool(st.session_state.demo_trading_armed),
            demo_pilot_preset=st.session_state.demo_pilot_preset,
        )
        st.session_state.runtime_key = runtime_key
        st.session_state.running = False
        saved.selected_profile = selected_profile
        saved.symbol = symbol
        saved.interval = interval
        saved.scenario = scenario
        saved.source = source
        saved.model_alias = model_alias
        store.save(saved)
    if "runtime" not in st.session_state:
        st.session_state.runtime = create_runtime(
            runtime_settings,
            mode,
            symbol,
            interval,
            scenario,
            7,
            max_daily_loss,
            max_position,
            int(max_trades),
            float(min_conf),
            max_spread,
            source,
            model_alias,
            int(max_data_age_ms),
            default_quote_size,
            bool(st.session_state.demo_trading_armed),
            demo_pilot_preset=st.session_state.demo_pilot_preset,
        )
        st.session_state.runtime_key = runtime_key
        st.session_state.running = False
    if start:
        st.session_state.running = True
    if pause:
        st.session_state.running = False
    if emergency_stop:
        st.session_state.running = False
        st.session_state.multi_demo_running = False
        for multi_runtime in st.session_state.get("multi_demo_runtimes", {}).values():
            multi_runtime.stop()
        st.session_state.runtime.stop()
    if step_once:
        st.session_state.runtime.step()
    if st.session_state.running:
        st.session_state.runtime.run_steps(int(speed))
    snapshot = st.session_state.runtime.snapshot()
    _render_status_header(snapshot, profile, runtime_settings, saved)
    if simple_dashboard:
        _render_simple_demo_dashboard(
            st.session_state.runtime,
            snapshot,
            st.session_state.credential_manager,
            runtime_settings,
            selected_profile,
            symbol,
            interval,
            scenario,
            source,
            model_alias,
            max_daily_loss,
            max_position,
            int(max_trades),
            float(min_conf),
            max_spread,
            int(max_data_age_ms),
            default_quote_size,
            saved,
            store,
        )
        return

    with tabs[0]:
        _render_overview(snapshot, profile, runtime_settings)
    with tabs[1]:
        _render_demo_spot_trading(runtime_settings, snapshot, symbol, interval)
    with tabs[2]:
        _render_credentials(st.session_state.credential_manager, runtime_settings, selected_profile, symbol)
    with tabs[3]:
        _render_bot_controls(snapshot, st.session_state.running, runtime_key)
    with tabs[5]:
        _render_strategy(snapshot, runtime_settings)
    with tabs[6]:
        _render_market(snapshot)
    with tabs[7]:
        _render_orders(snapshot)
    with tabs[8]:
        _render_sessions(snapshot)
    with tabs[9]:
        _render_evaluation(snapshot, runtime_settings, symbol, interval)
    with tabs[10]:
        _render_strategy_lab(snapshot)
    with tabs[11]:
        _render_research(snapshot, runtime_settings)
    with tabs[12]:
        _render_portfolio(snapshot)
    with tabs[13]:
        _render_readiness(snapshot)
    with tabs[14]:
        _render_logs_security(snapshot, runtime_settings)
    with tabs[15]:
        _render_demo_pilot(st.session_state.runtime, snapshot)
    with tabs[16]:
        _render_policy_governance()
    with tabs[17]:
        _render_ops_automation(runtime_settings)
    with tabs[18]:
        _render_observability(runtime_settings)
    with tabs[19]:
        _render_ai_ops_assistant(runtime_settings)
    with tabs[20]:
        _render_action_center(runtime_settings)
    with tabs[21]:
        _render_permissions(runtime_settings)
    with tabs[22]:
        _render_disaster_recovery(runtime_settings)
    with tabs[23]:
        _render_release_management()
    with tabs[24]:
        _render_roadmap_automation()
    with tabs[25]:
        _render_repo_knowledge()
    with tabs[26]:
        _render_test_selection()
    with tabs[27]:
        _render_performance()
    with tabs[28]:
        _render_runtime_core()
    with tabs[29]:
        _render_data_pipeline()
    with tabs[30]:
        _render_model_training()
    with tabs[31]:
        _render_model_monitoring()
    with tabs[32]:
        _render_portfolio_ensemble()
    with tabs[33]:
        _render_paper_os_audit()
    with tabs[34]:
        _render_stabilization()
    with tabs[35]:
        _render_operator_training()

    if st.session_state.running and snapshot.status not in {"completed", "stopped"}:
        time.sleep(2.0)
        st.rerun()


def _render_policy_governance() -> None:
    st.subheader("Paper Policy Governance")
    st.caption("PAPER GOVERNANCE ONLY")
    result = run_governance_simulation("challenger_beats")
    decision = result["decision"]
    stop = result["stopping"]
    metrics = result["experiment"]["metrics"]
    cols = st.columns(4)
    cols[0].metric("Decision", decision["decision"])
    cols[1].metric("Stop status", stop["status"])
    cols[2].metric("Champion observations", metrics["champion"]["observations"])
    cols[3].metric("Challenger observations", metrics["challenger"]["observations"])
    render_badges(
        [
            {"label": "Live trading", "value": "disabled", "status": "ok"},
            {"label": "Signed endpoints", "value": "not used", "status": "ok"},
            {"label": "Mode", "value": "paper only", "status": "ok"},
        ]
    )
    render_table(
        "Champion / Challenger Metrics",
        [
            {"variant": name, **row}
            for name, row in metrics.items()
        ],
    )
    with st.expander("Governance evidence"):
        st.json(result)


def _render_ops_automation(settings: BotSettings) -> None:
    st.subheader("Local Paper Ops Automation")
    st.caption("LOCAL PAPER OPS ONLY")
    report = generate_scheduled_ops_report(settings)
    render_badges({"Status": report["status"], "Jobs": len(report["schedule"]["jobs"]), "Live trading": "disabled"})
    render_table("Scheduled Jobs", report["schedule"]["jobs"])
    with st.expander("Runbook evidence"):
        st.json(report)


def _render_observability(settings: BotSettings) -> None:
    st.subheader("Local Observability")
    st.caption("LOCAL OBSERVABILITY ONLY")
    report = write_metrics_report(settings, [{"equity": 1000, "pnl_quote": 0, "latency_ms": 25}])
    render_badges({"Status": report["status"], "Rows": report["rows"], "Live trading": "disabled"})
    render_table("Metric Aggregates", [{"metric": key, **value} for key, value in report["metrics"].items()])
    with st.expander("Metrics evidence"):
        st.json(report)


def _render_ai_ops_assistant(settings: BotSettings) -> None:
    st.subheader("AI Ops Assistant")
    st.caption("AI OPS ASSISTANT - READ ONLY")
    question = st.text_input("Question", value="Wat is de bot status?", key="ai_ops_question")
    answer = answer_ops_question(settings, question)
    render_badges({"Status": answer["status"], "Sources": len(answer["sources"]), "Live trading": "disabled"})
    st.write(answer["answer"])


def _render_action_center(settings: BotSettings) -> None:
    st.subheader("Human In The Loop Action Center")
    st.caption("HUMAN-IN-THE-LOOP REQUIRED - NO LIVE TRADING")
    workflow = ApprovalWorkflow(settings.data_dir, data_dir=settings.data_dir)
    queue = ApprovalQueueStore(settings.data_dir / "action-center")
    records = queue.list_queue()
    render_badges(
        {
            "Open proposals": len([record for record in records if record.status not in {"completed", "rejected", "expired"}]),
            "Total proposals": len(records),
            "Live trading": "disabled",
        }
    )
    with st.form("action_center_new_proposal"):
        command = st.selectbox("Safe local action", ["diagnostics", "operator-report", "support-bundle", "support-bundles-verify", "dashboard-smoke"], key="action_center_command")
        safety = st.selectbox("Safety class", [item.value for item in ActionSafetyClass if item != ActionSafetyClass.FORBIDDEN], key="action_center_safety")
        reason = st.text_input("Reason", value="operator requested local evidence", key="action_center_reason")
        submitted = st.form_submit_button("Send to approval queue")
    if submitted:
        proposal = proposal_from_command(command, ["--json"] if command != "dashboard-smoke" else ["--seconds", "1"], title=command, description=reason, source="dashboard", safety_class=safety)
        st.session_state.action_center_last = workflow.submit(proposal)
    if st.session_state.get("action_center_last"):
        st.success(f"Proposal status: {st.session_state.action_center_last['status']}")
    rows = [
        {
            "proposal_id": record.proposal.proposal_id,
            "title": record.proposal.title,
            "status": record.status,
            "safety": record.proposal.safety_class.value,
            "command": record.proposal.command.preview(),
        }
        for record in records[:25]
    ]
    render_table("Approval queue", rows)
    selected = st.selectbox("Proposal detail", [""] + [record.proposal.proposal_id for record in records[:25]], key="action_center_selected")
    if selected:
        record = queue.load(selected)
        st.write("Command preview")
        st.code(record.proposal.command.preview())
        confirm = st.text_input("Confirm phrase", value="", key=f"action_center_confirm_{selected}")
        c1, c2, c3 = st.columns(3)
        if c1.button("Approve", key=f"action_center_approve_{selected}", use_container_width=True):
            st.session_state.action_center_decision = workflow.decide(selected, "approve", confirm_phrase=confirm, reason="dashboard approval")
        if c2.button("Reject", key=f"action_center_reject_{selected}", use_container_width=True):
            st.session_state.action_center_decision = workflow.decide(selected, "reject", reason="dashboard rejection")
        if c3.button("Defer", key=f"action_center_defer_{selected}", use_container_width=True):
            st.session_state.action_center_decision = workflow.decide(selected, "defer", reason="dashboard defer")
        with st.expander("Raw proposal"):
            st.json(record.to_dict())
    journal_rows = DecisionJournal(settings.data_dir / "action-center").entries(limit=20)
    render_table("Decision journal", journal_rows)


def _render_permissions(settings: BotSettings) -> None:
    st.subheader("Permissions & Compliance")
    st.caption("LOCAL PERMISSIONS ONLY - NO LIVE TRADING")
    report = permission_compliance_report(settings)
    identity = local_operator_identity()
    drift = permission_drift({"manifest": report["matrix"]["manifest_hash"]}, {"manifest": report["matrix"]["manifest_hash"]})
    score_report = write_compliance_report(settings.data_dir)
    render_badges(
        {
            "Status": report["status"],
            "Operator": identity["identity"]["display_name"],
            "Drift": drift["status"],
            "Compliance": score_report["compliance_score"]["grade"],
            "Live trading": "disabled",
        }
    )
    render_table("Profiles", list(report["matrix"]["profiles"].values()))
    render_table("Permission drift", drift.get("findings", []))
    with st.expander("Compliance report"):
        st.json(score_report)


def _render_disaster_recovery(settings: BotSettings) -> None:
    st.subheader("Disaster Recovery")
    st.caption("OFFLINE DR ONLY")
    profiles = backup_profiles()
    integrity = state_integrity_check(settings.data_dir)
    report = run_disaster_recovery_drill(settings)
    render_badges(
        {
            "Status": report["status"],
            "Profiles": len(profiles["profiles"]),
            "Integrity": integrity["status"],
            "Backup verify": report["backup_verify"]["status"],
            "Restore drill": report["restore_drill"]["status"],
            "Live trading": "disabled",
        }
    )
    render_table("Backup profiles", list(profiles["profiles"].values()))
    render_table("State integrity", integrity.get("issues", []))
    with st.expander("DR evidence"):
        st.json(report)


def _render_release_management() -> None:
    st.subheader("Release Management")
    st.caption("LOCAL RELEASE ONLY - NO LIVE TRADING")
    payload = version_payload("local")
    from binance_spot_bot.release_candidate import release_candidate
    from binance_spot_bot.release_quality_gate import release_quality_gate

    candidate = release_candidate("0.2.0")
    gate = release_quality_gate([candidate])
    render_badges({"Version": payload["payload"]["version"], "Schema": payload["payload"]["schema_version"], "Candidate": candidate["status"], "Gate": gate["status"], "Live trading": "disabled"})
    with st.expander("Release candidate"):
        st.json(candidate)


def _render_roadmap_automation() -> None:
    st.subheader("Roadmap Execution")
    st.caption("ROADMAP EXECUTION ONLY - EVIDENCE GATED - NO LIVE TRADING")
    from binance_spot_bot.codex_task_pack_generator import generate_codex_task_packs
    from binance_spot_bot.pr_template_generator import generate_pr_template
    from binance_spot_bot.roadmap_completion_gate import evaluate_roadmap_completion_gate
    from binance_spot_bot.roadmap_duplicate_guard import run_roadmap_duplicate_guard
    from binance_spot_bot.roadmap_quality_score import roadmap_quality_score

    payload = build_roadmap_index(Path.cwd())
    guard = run_roadmap_duplicate_guard(Path.cwd())
    open_roadmaps = payload["payload"].get("roadmaps", [])
    selected = next((item for item in open_roadmaps if item.get("location") == "roadmap_docs"), None)
    roadmap_number = selected.get("number", 0) if selected else 0
    roadmap_path = Path.cwd() / selected["path"] if selected else None
    text = roadmap_path.read_text(encoding="utf-8-sig", errors="ignore") if roadmap_path and roadmap_path.exists() else ""
    score = roadmap_quality_score(text)
    gate = evaluate_roadmap_completion_gate(
        f"{roadmap_number:03d}" if roadmap_number else "000",
        evidence={"tests_passed": False, "check_all_passed": False, "no_live_proof": True},
        dashboard_touched=True,
    )
    render_badges(
        {
            "Open": payload["payload"]["open_count"],
            "Done": payload["payload"]["done_count"],
            "Next": payload["payload"]["next_number"],
            "Guard": guard["status"],
            "Score": score["grade"],
            "Gate": gate["status"],
            "Live trading": "disabled",
        }
    )
    render_table(
        "Open roadmaps",
        [
            {"number": item.get("number"), "title": item.get("title"), "status": item.get("status")}
            for item in open_roadmaps
            if item.get("location") == "roadmap_docs"
        ][:12],
    )
    with st.expander("Task pack preview"):
        st.json(generate_codex_task_packs(Path.cwd(), roadmap_number or payload["payload"]["next_number"]))
    with st.expander("PR template preview"):
        st.markdown(generate_pr_template(roadmap_number or payload["payload"]["next_number"], "foundation")["markdown"])
    with st.expander("Guard and completion JSON"):
        st.json({"duplicate_guard": guard, "completion_gate": gate, "quality_score": score, "live_trading_enabled": False})


def _render_repo_knowledge() -> None:
    st.subheader("Repo Knowledge")
    st.caption("LOCAL REPOSITORY KNOWLEDGE ONLY - NO LIVE TRADING")
    from binance_spot_bot.cli_surface_map import build_cli_surface_map
    from binance_spot_bot.code_graph import build_code_graph
    from binance_spot_bot.dashboard_surface_map import build_dashboard_surface_map
    from binance_spot_bot.impact_analysis import impact_analysis
    from binance_spot_bot.repo_knowledge_report import build_repo_knowledge_report

    payload = repo_inventory(Path.cwd())
    files = payload["payload"]["files"]
    graph = build_code_graph(Path.cwd())
    cli_map = build_cli_surface_map(Path.cwd())
    dashboard_map = build_dashboard_surface_map(Path.cwd())
    impact = impact_analysis(["src/binance_spot_bot/runtime.py"])
    report = build_repo_knowledge_report(Path.cwd())
    render_badges(
        {
            "Files": len(files),
            "Python modules": len(graph["payload"]["nodes"]),
            "CLI commands": cli_map["payload"]["count"],
            "Dashboard panels": len(dashboard_map["payload"]["panels"]),
            "Impact": impact["risk"]["payload"]["level"],
            "Live trading": "disabled",
        }
    )
    render_table(
        "Safety-relevant files",
        [
            {"path": item["path"], "category": item["category"], "lines": item["line_count"]}
            for item in files
            if item["safety_relevant_guess"]
        ][:12],
    )
    with st.expander("Recommended tests for runtime.py"):
        st.json(impact["tests"])
    with st.expander("Repository knowledge report"):
        st.json(report)


def _render_test_selection() -> None:
    st.subheader("Test Selection & Regression Risk")
    st.caption("LOCAL TEST SELECTION ONLY - NO LIVE TRADING")
    from binance_spot_bot.flaky_tests import flaky_tests
    from binance_spot_bot.regression_risk_report import build_regression_risk_report
    from binance_spot_bot.test_profiles import test_profiles
    from binance_spot_bot.test_runtime_history import summarize_test_runtime_history

    changed = ["src/binance_spot_bot/runtime.py"]
    payload = selected_tests(changed)
    report = build_regression_risk_report(changed)
    history = summarize_test_runtime_history(Path.cwd())
    render_badges(
        {
            "Profile": payload["selected_profile"],
            "Risk": payload["risk"]["level"],
            "Commands": len(payload["selected_commands"]),
            "History": history["count"],
            "Live trading": "disabled",
        }
    )
    render_table("Selected commands", [{"command": command} for command in payload["selected_commands"]])
    with st.expander("Regression risk report"):
        st.json(report)
    with st.expander("Profiles and flaky status"):
        st.json({"profiles": test_profiles(), "flaky": flaky_tests([{"command": "pytest", "status": "ok"}]), "live_trading_enabled": False})


def _render_performance() -> None:
    st.subheader("Performance")
    st.caption("LOCAL RESOURCE BUDGETS")
    payload = performance_budget(10, 20)
    render_badges({"Status": payload["status"], "Actual ms": payload["actual_ms"], "Budget ms": payload["budget_ms"]})


def _render_runtime_core() -> None:
    st.subheader("Runtime Core")
    st.caption("EVENTED SNAPSHOT SURFACE")
    payload = build_runtime_snapshot({"status": "ready", "events": 0})
    st.json(payload)


def _render_data_pipeline() -> None:
    st.subheader("Data Pipeline")
    st.caption("FEATURE CONTRACTS")
    payload = data_quality_v2([{"close": 1}])
    render_badges({"Status": payload["status"], "Rows": payload["rows"], "Live trading": "disabled"})


def _render_model_training() -> None:
    st.subheader("Model Training")
    st.caption("FEATURE CONTRACT AWARE")
    payload = run_training_pipeline(25)
    render_badges({"Gate": payload["gate"]["status"], "Rows": payload["training"]["payload"]["rows"], "Live trading": "disabled"})


def _render_model_monitoring() -> None:
    st.subheader("Model Monitoring")
    st.caption("SHADOW PAPER ONLY")
    payload = model_health_score(0.1, performance_ok=True)
    render_badges({"Status": payload["status"], "Score": payload["score"], "Live trading": "disabled"})


def _render_portfolio_ensemble() -> None:
    st.subheader("Portfolio Ensemble")
    st.caption("PAPER ALLOCATION ONLY")
    payload = ensemble_prediction([{"signal": "BUY", "confidence": 0.7}, {"signal": "HOLD", "confidence": 0.5}])
    render_badges({"Signal": payload["payload"]["signal"], "Confidence": payload["payload"]["confidence"], "Live trading": "disabled"})


def _render_paper_os_audit() -> None:
    st.subheader("Paper OS Audit")
    st.caption("PRODUCTION READINESS SIMULATION")
    payload = paper_os_simulation()
    render_badges({"Status": payload["payload"]["status"], "Invariants": len(payload["payload"]["invariants"]), "Live trading": "disabled"})


def _render_stabilization() -> None:
    st.subheader("Stabilization")
    st.caption("BLOCKER BURN DOWN")
    payload = stabilization_gate([], [])
    render_badges({"Status": payload["status"], "Live trading": "disabled"})


def _render_operator_training() -> None:
    st.subheader("Operator Training")
    st.caption("LOCAL PAPER OS MANUAL")
    payload = operator_glossary()
    render_table("Glossary", [{"term": key, "meaning": value} for key, value in payload["terms"].items()])


def _render_status_header(snapshot, profile, settings: BotSettings, saved) -> None:
    runner_status = PilotRunnerService(settings).status()
    runner = runner_status.get("runner", {})
    render_badges(
        {
            "Live": "disabled" if not settings.live_trading_enabled else "blocked",
            "Mode": snapshot.mode,
            "Source": snapshot.market_data.get("source", "unknown"),
            "Workspace": "default",
            "Profile": profile.mode_badge,
            "Base URL": settings.active_base_url,
            "Kill switch": "on" if settings.kill_switch else "paper override",
            "Demo armed": "yes" if snapshot.demo_connection.get("armed") else "no",
            "Runner": runner.get("state", "not_running"),
            "Session": snapshot.status,
            "Readiness": snapshot.readiness.get("level", "R0"),
        }
    )
    if st.button("Export operator evidence", key="operator_evidence_export", use_container_width=True):
        payload = build_operator_evidence(
            settings,
            mode=snapshot.mode,
            profile=profile.name,
            source=snapshot.market_data.get("source", "unknown"),
            snapshot=snapshot,
            connectivity=st.session_state.get("connectivity_report", {}),
            runner_status=runner_status,
        )
        path = write_operator_evidence(settings, payload)
        st.session_state.operator_evidence_path = str(path)
    if st.session_state.get("operator_evidence_path"):
        st.caption(f"Operator evidence: {st.session_state.operator_evidence_path}")
    if snapshot.readiness.get("blockers"):
        st.warning("Readiness blockers: " + ", ".join(snapshot.readiness["blockers"]))


def _render_overview(snapshot, profile, settings: BotSettings) -> None:
    st.subheader("Operational overview")
    state = DashboardRuntimeState(
        DashboardProcessStatus.RUNNING,
        bot_status_from_runtime(snapshot.status),
        snapshot.mode,
        snapshot.market_data.get("source", "unknown"),
        profile.name,
        live_disabled=not settings.live_trading_enabled,
    )
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Profile", profile.mode_badge)
    c2.metric("Runtime", snapshot.mode)
    c3.metric("Status", snapshot.status)
    c4.metric("Equity", f"{snapshot.equity}")
    c5.metric("Position", f"{snapshot.paper_position}")
    c6.metric("Live", "disabled")
    st.info(f"{snapshot.message} | Base URL: {settings.active_base_url} | Live trading is not selectable.")
    chart_col, side_col = st.columns([3, 1])
    with chart_col:
        render_plotly_chart(
            candlestick_figure(
                snapshot.candles,
                snapshot.signals,
                snapshot.fills,
                open_orders=snapshot.demo_open_orders,
                reconciliation_events=snapshot.reconciliation.get("events", []),
            ),
            key=OVERVIEW_CANDLESTICK,
        )
        render_plotly_chart(equity_figure(snapshot.equity_points), key=OVERVIEW_EQUITY)
    with side_col:
        render_debug("Health details", snapshot.metrics.health())
        render_debug("Credential status", snapshot.credential_status)
        st.subheader("Start wizard")
        render_debug("Wizard options", {"state": state.to_dict(), "options": wizard_options()})
        st.subheader("Workspace")
        workspace_store = WorkspaceStore(settings.data_dir / "workspaces")
        if st.button("Save current workspace"):
            workspace_store.save(WorkspaceProfile("default", str(settings.data_dir), profile.name, [snapshot.symbol], language="nl"))
        render_table("Saved workspaces", [workspace.to_dict() for workspace in workspace_store.list()])


def _render_simple_demo_dashboard(
    runtime,
    snapshot,
    manager: CredentialManager,
    settings: BotSettings,
    selected_profile: str,
    symbol: str,
    interval: str,
    scenario: str,
    source: str,
    model_alias: str,
    max_daily_loss: Decimal,
    max_position: Decimal,
    max_trades: int,
    min_conf: float,
    max_spread: Decimal,
    max_data_age_ms: int,
    default_quote_size: Decimal,
    saved,
    store,
) -> None:
    st.subheader("Start Demo Trading")
    st.caption("Simple mode voor Binance Demo Spot. Kies een of meerdere crypto-symbolen en start ze samen. Advanced tools: Overview, Demo Spot Trading, Demo Pilot.")
    profile = available_profiles()[selected_profile]
    credential_status = manager.status()
    connection = st.session_state.get("connectivity_report", {})
    connection_status = connection.get("status", "not-tested")
    armed = bool(snapshot.demo_connection.get("armed"))
    can_arm = selected_profile == BINANCE_DEMO_SPOT_PROFILE and credential_status.has_api_key and credential_status.has_api_secret
    has_keys = credential_status.has_api_key and credential_status.has_api_secret
    render_badges(
        {
            "Profile": profile.label,
            "Mode": "Demo Binance Spot",
            "Symbol": symbol,
            "Interval": interval,
            "Keys": "loaded" if credential_status.has_api_key and credential_status.has_api_secret else "missing",
            "Connected": connection_status,
            "Trading": "armed" if armed else "not armed",
            "Bots": "running" if st.session_state.multi_demo_running else snapshot.status,
            "Live": "disabled",
        }
    )
    with st.form("simple_demo_credentials"):
        st.write("Binance demo keys")
        api_key = st.text_input("API key", value="", type="password", key="simple_demo_api_key")
        api_secret = st.text_input("API secret", value="", type="password", key="simple_demo_api_secret")
        save_keys = st.form_submit_button("Use demo keys for this session")
    if save_keys:
        manager.set_session_credentials(selected_profile, api_key, api_secret)
        st.session_state.demo_trading_armed = False
        st.session_state.multi_demo_running = False
        st.success("Demo keys loaded for this Streamlit session.")
        st.rerun()

    st.subheader("Multi Crypto Demo Trading")
    default_watchlist = saved.watchlist if getattr(saved, "watchlist", None) else list(DEFAULT_DEMO_SYMBOLS[:3])
    selected_symbols = st.multiselect(
        "Crypto symbols",
        list(DEFAULT_DEMO_SYMBOLS),
        default=[item for item in default_watchlist if item in DEFAULT_DEMO_SYMBOLS] or ([symbol] if symbol in DEFAULT_DEMO_SYMBOLS else list(DEFAULT_DEMO_SYMBOLS[:3])),
        key="simple_multi_symbols",
    )
    custom_symbols = st.text_input("Extra symbols", value="", placeholder="Bijvoorbeeld: AVAXUSDT, MATICUSDT, DOT", key="simple_custom_symbols")
    max_active_symbols = st.number_input("Max active symbols", min_value=1, max_value=10, value=min(3, max(1, len(selected_symbols) or 1)), step=1)
    max_open_orders_per_symbol = st.number_input("Max open orders per symbol", min_value=1, max_value=10, value=2, step=1)
    total_quote_budget = Decimal(str(st.number_input("Total demo quote budget", min_value=10.0, value=1000.0, step=50.0)))
    candle_window = st.slider("Visible candles", min_value=20, max_value=120, value=40, step=10)
    st.subheader("Adaptive Indicator Advisor")
    auto_indicator_profile = st.checkbox("Auto-select indicator profile", value=True, key="auto_indicator_profile")
    indicator_profile = st.selectbox(
        "Indicator profile",
        list(INDICATOR_PROFILES),
        index=0,
        disabled=auto_indicator_profile,
        key="indicator_profile",
    )
    active_symbols = choose_active_symbols(selected_symbols or [symbol], custom_symbols, max_active=int(max_active_symbols))
    validation = validate_demo_symbols(active_symbols, max_active=int(max_active_symbols))
    ready = can_arm and armed and connection_status in {"ok", "warn", "not-tested"} and validation["status"] != "fail"
    allocation = allocation_plan(
        active_symbols,
        total_quote_budget=total_quote_budget,
        default_quote_size=default_quote_size,
        max_position_quote=max_position,
    )
    risk_rows = risk_limit_rows(
        active_symbols,
        max_open_orders_per_symbol=int(max_open_orders_per_symbol),
        max_trades=max_trades,
        max_position_quote=max_position,
        max_daily_loss=max_daily_loss,
        max_spread=max_spread,
        min_conf=min_conf,
    )
    next_action = next_multi_action(
        has_keys=has_keys,
        connection_status=connection_status,
        armed=armed,
        validation_status=str(validation["status"]),
        running=bool(st.session_state.multi_demo_running),
    )
    st.info(f"Next step: {next_action}")
    st.caption("Elke crypto krijgt een eigen demo-runtime met eigen risk checks en eigen open-order overzicht.")
    preset_cols = st.columns(2)
    if preset_cols[0].button("Save active watchlist", use_container_width=True):
        saved.watchlist = active_symbols
        store.save(saved)
        st.success("Watchlist saved locally without secrets.")
    if preset_cols[1].button("Reset watchlist preset", use_container_width=True):
        saved.watchlist = list(DEFAULT_DEMO_SYMBOLS[:3])
        store.save(saved)
        st.rerun()
    render_table("Symbol validation guardrails", [*validation.get("blockers", []), *validation.get("warnings", [])])

    actions = st.columns(4)
    if actions[0].button("Test demo connection", use_container_width=True, disabled=not (credential_status.has_api_key and credential_status.has_api_secret)):
        checked = manager.apply_to_settings(settings, selected_profile)
        st.session_state.connectivity_report = connectivity_report(checked, symbol)
        st.rerun()
    if actions[1].button("Connect demo trading", use_container_width=True, disabled=not can_arm):
        st.session_state.demo_trading_armed = True
        st.rerun()
    if actions[2].button("Start selected symbols", use_container_width=True, type="primary", disabled=not ready or not active_symbols):
        try:
            _sync_multi_demo_runtimes(
                settings,
                active_symbols,
                interval,
                scenario,
                source,
                model_alias,
                max_daily_loss,
                max_position,
                max_trades,
                min_conf,
                max_spread,
                max_data_age_ms,
                default_quote_size,
                max_open_orders_per_symbol=int(max_open_orders_per_symbol),
                demo_trading_armed=True,
            )
            for multi_runtime in st.session_state.multi_demo_runtimes.values():
                multi_runtime.start()
            st.session_state.multi_demo_running = True
        except (OSError, ValueError) as exc:
            st.session_state.simple_demo_error = str(exc)
        st.rerun()
    if actions[3].button("Stop all symbols", use_container_width=True):
        st.session_state.running = False
        st.session_state.multi_demo_running = False
        for multi_runtime in st.session_state.get("multi_demo_runtimes", {}).values():
            multi_runtime.stop()
        st.rerun()
    stop_symbol = st.text_input("Stop one symbol", value="", placeholder="Bijvoorbeeld ETH of ETHUSDT", key="simple_stop_one_symbol")
    if st.button("Stop selected symbol only", use_container_width=True):
        stopped = _stop_one_multi_symbol(stop_symbol)
        st.session_state.simple_demo_error = "" if stopped else f"Symbol not running: {stop_symbol}"
        st.rerun()

    if st.session_state.get("simple_demo_error"):
        st.error(st.session_state.simple_demo_error)
    live_panel_updates = st.toggle(
        "Live status panel",
        value=True,
        key="simple_live_status_panel",
        help="Only this live panel refreshes every 2 seconds; the full dashboard does not rerun.",
    )
    if live_panel_updates:
        _render_simple_live_fragment(
            settings,
            snapshot,
            active_symbols,
            interval,
            scenario,
            source,
            model_alias,
            max_daily_loss,
            max_position,
            max_trades,
            min_conf,
            max_spread,
            max_data_age_ms,
            default_quote_size,
            int(max_open_orders_per_symbol),
            allocation,
            risk_rows,
            validation,
            credential_status.has_api_key and credential_status.has_api_secret,
            connection_status,
            armed,
            candle_window,
            "auto" if auto_indicator_profile else indicator_profile,
            bool(auto_indicator_profile),
            total_quote_budget,
        )
    else:
        if st.button("Refresh live status once", use_container_width=True):
            _advance_multi_demo_once(
                settings,
                active_symbols,
                interval,
                scenario,
                source,
                model_alias,
                max_daily_loss,
                max_position,
                max_trades,
                min_conf,
                max_spread,
                max_data_age_ms,
                default_quote_size,
                int(max_open_orders_per_symbol),
            )
        _render_simple_live_content(
            settings,
            snapshot,
            active_symbols,
            allocation,
            risk_rows,
            validation,
            credential_status.has_api_key and credential_status.has_api_secret,
            connection_status,
            armed,
            candle_window,
            "auto" if auto_indicator_profile else indicator_profile,
            bool(auto_indicator_profile),
            total_quote_budget,
        )
    with st.expander("Simple multi-symbol help"):
        st.write("Gebruik eerst demo keys, test de verbinding, connect demo trading en start daarna alleen de geselecteerde symbolen.")
        st.write("Elke crypto draait in een aparte demo-runtime. Stop one symbol stopt alleen die runtime; Stop all symbols stopt alles.")
    if connection:
        with st.expander("Connection details"):
            render_debug("Connectivity report", connection)


@st.fragment(run_every="2s")
def _render_simple_live_fragment(
    settings: BotSettings,
    snapshot,
    active_symbols: list[str],
    interval: str,
    scenario: str,
    source: str,
    model_alias: str,
    max_daily_loss: Decimal,
    max_position: Decimal,
    max_trades: int,
    min_conf: float,
    max_spread: Decimal,
    max_data_age_ms: int,
    default_quote_size: Decimal,
    max_open_orders_per_symbol: int,
    allocation: list[dict[str, str]],
    risk_rows: list[dict[str, object]],
    validation: dict[str, object],
    has_keys: bool,
    connection_status: str,
    armed: bool,
    candle_window: int,
    indicator_profile: str,
    auto_indicator_profile: bool,
    total_quote_budget: Decimal,
) -> None:
    _advance_multi_demo_once(
        settings,
        active_symbols,
        interval,
        scenario,
        source,
        model_alias,
        max_daily_loss,
        max_position,
        max_trades,
        min_conf,
        max_spread,
        max_data_age_ms,
        default_quote_size,
        max_open_orders_per_symbol,
    )
    _render_simple_live_content(
        settings,
        snapshot,
        active_symbols,
        allocation,
        risk_rows,
        validation,
        has_keys,
        connection_status,
        armed,
        candle_window,
        indicator_profile,
        auto_indicator_profile,
        total_quote_budget,
    )


def _advance_multi_demo_once(
    settings: BotSettings,
    active_symbols: list[str],
    interval: str,
    scenario: str,
    source: str,
    model_alias: str,
    max_daily_loss: Decimal,
    max_position: Decimal,
    max_trades: int,
    min_conf: float,
    max_spread: Decimal,
    max_data_age_ms: int,
    default_quote_size: Decimal,
    max_open_orders_per_symbol: int,
) -> None:
    if not st.session_state.multi_demo_running:
        return
    _sync_multi_demo_runtimes(
        settings,
        active_symbols,
        interval,
        scenario,
        source,
        model_alias,
        max_daily_loss,
        max_position,
        max_trades,
        min_conf,
        max_spread,
        max_data_age_ms,
        default_quote_size,
        max_open_orders_per_symbol=max_open_orders_per_symbol,
        demo_trading_armed=True,
    )
    for multi_runtime in list(st.session_state.multi_demo_runtimes.values()):
        if multi_runtime.status == "completed":
            _restart_completed_multi_runtime(
                settings,
                multi_runtime.options.symbol,
                interval,
                scenario,
                source,
                model_alias,
                max_daily_loss,
                max_position,
                max_trades,
                min_conf,
                max_spread,
                max_data_age_ms,
                default_quote_size,
            )
        elif multi_runtime.status != "stopped":
            multi_runtime.run_steps(2)


def _render_simple_live_content(
    settings: BotSettings,
    snapshot,
    active_symbols: list[str],
    allocation: list[dict[str, str]],
    risk_rows: list[dict[str, object]],
    validation: dict[str, object],
    has_keys: bool,
    connection_status: str,
    armed: bool,
    candle_window: int,
    indicator_profile: str,
    auto_indicator_profile: bool,
    total_quote_budget: Decimal,
) -> None:
    st.caption("Live status updates run inside this panel only; the full dashboard stays stable.")
    multi_rows = _multi_demo_rows()
    if st.session_state.multi_demo_running and multi_rows and all(row["status"] == "stopped" for row in multi_rows):
        st.session_state.multi_demo_running = False
    summary = summarize_multi_rows(multi_rows)
    render_badges(
        {
            "Selected symbols": len(active_symbols),
            "Active bots": summary["active_bots"],
            "Total fills": summary["total_fills"],
            "Open orders": summary["total_open_orders"],
            "Live panel": "fragment",
        }
    )
    render_table(
        "Setup checklist",
        [
            {"step": "Demo profile", "status": "ok"},
            {"step": "Demo keys", "status": "ok" if has_keys else "missing"},
            {"step": "Connection test", "status": connection_status},
            {"step": "Demo trading connected", "status": "yes" if armed else "no"},
            {"step": "Symbols selected", "status": ", ".join(active_symbols) if active_symbols else "none"},
            {"step": "Multi bot running", "status": "yes" if st.session_state.multi_demo_running else "no"},
        ],
    )
    render_table("Multi crypto bot status", multi_rows)
    render_plotly_chart(multi_symbol_overview_figure(multi_rows), key="multi_symbol_visual_overview")
    indicator_rows = indicator_rows_from_runtimes(st.session_state.get("multi_demo_runtimes", {}), indicator_profile)
    indicator_payload = indicator_summary(indicator_rows)
    render_badges(
        {
            "Indicator profile": indicator_profile,
            "Auto profile": str(auto_indicator_profile),
            "Indicator symbols": indicator_payload["symbols"],
            "Avg confidence": indicator_payload["avg_confidence"],
        }
    )
    with st.expander("Binance public data controls"):
        public_limit = st.number_input("Public candle limit", min_value=30, max_value=1000, value=120, step=10)
        if st.button("Fetch Binance public data", use_container_width=True, key="fetch_binance_public_data_live_panel"):
            st.session_state.public_data_warmup = warmup_indicators(
                settings,
                active_symbols,
                candle_limit=int(public_limit),
            )
        if st.button("Warm up indicators", use_container_width=True, key="warmup_indicators_live_panel"):
            st.session_state.public_data_warmup = warmup_indicators(
                settings,
                active_symbols,
                candle_limit=int(public_limit),
            )
        if st.button("Show cache status", use_container_width=True, key="public_data_cache_status_live_panel"):
            from binance_spot_bot.binance_data_ingestion import BinanceDataIngestionService

            st.session_state.public_data_cache_status = BinanceDataIngestionService(settings).cache_status()
        if st.button("Export public data evidence", use_container_width=True, key="export_public_data_evidence_live_panel"):
            from binance_spot_bot.binance_data_ingestion import export_public_data_evidence

            st.session_state.public_data_evidence = {"path": str(export_public_data_evidence(settings))}
        render_debug("Public data warmup status", st.session_state.get("public_data_warmup", {}))
        render_debug("Public data cache status", st.session_state.get("public_data_cache_status", {}))
        render_debug("Public data evidence", st.session_state.get("public_data_evidence", {}))
    render_table("Adaptive indicator advisor", indicator_rows)
    render_table("Risk adjusted allocation hints", allocation_hints(indicator_rows, total_quote_budget))
    with st.expander("Bot trading decision explanation"):
        render_table(
            "Indicator decision reasons",
            [
                {
                    "symbol": row.get("symbol"),
                    "bias": row.get("bias"),
                    "confidence": row.get("confidence"),
                    "reason": row.get("reason"),
                    "risk_engine": "still authoritative",
                }
                for row in indicator_rows
            ],
        )
        render_debug("Indicator sanity summary", indicator_payload)
    if st.button("Export indicator evidence", use_container_width=True, key="export_indicator_evidence_live_panel"):
        st.session_state.indicator_evidence = write_indicator_evidence(
            settings.data_dir,
            indicator_rows,
            indicator_profile,
            auto_indicator_profile,
        )
    if st.session_state.get("indicator_evidence"):
        render_debug("Indicator evidence export", st.session_state.indicator_evidence)
    render_table("Budget allocation", allocation)
    render_table("Risk limit summary", risk_rows)
    if st.button("Export multi-symbol evidence", use_container_width=True, key="export_multi_symbol_evidence_live_panel"):
        st.session_state.multi_symbol_evidence = write_multi_symbol_evidence(
            settings.data_dir,
            symbols=active_symbols,
            rows=multi_rows,
            validation=validation,
            allocation=allocation,
            summary=summary,
        )
    if st.session_state.get("multi_symbol_evidence"):
        render_debug("Multi-symbol evidence export", st.session_state.multi_symbol_evidence)
    chart_symbols = [row["symbol"] for row in multi_rows] or active_symbols
    focus_symbol = st.selectbox("Chart focus symbol", chart_symbols, index=0, key="simple_chart_focus_symbol")
    primary_snapshot = _snapshot_for_symbol(str(focus_symbol)) or _primary_multi_snapshot() or snapshot
    focused_indicator = next((row for row in indicator_rows if row.get("symbol") == focus_symbol), {})
    if focused_indicator:
        render_badges(
            {
                "Focused regime": focused_indicator.get("regime", "-"),
                "Focused RSI": focused_indicator.get("rsi", "-"),
                "Focused bias": focused_indicator.get("bias", "-"),
                "Focused reason": focused_indicator.get("reason", "-"),
            }
        )
    metrics = st.columns(4)
    metrics[0].metric("Equity", str(primary_snapshot.equity))
    metrics[1].metric("Paper quote", str(primary_snapshot.paper_quote))
    metrics[2].metric("Fills", sum(int(row["fills"]) for row in multi_rows))
    metrics[3].metric("Open demo orders", sum(int(row["open_orders"]) for row in multi_rows))
    render_plotly_chart(
        candlestick_figure(
            primary_snapshot.candles[-candle_window:],
            primary_snapshot.signals[-candle_window:],
            primary_snapshot.fills[-candle_window:],
            open_orders=primary_snapshot.demo_open_orders,
            reconciliation_events=primary_snapshot.reconciliation.get("events", []),
        ),
        key="simple_demo_candlestick",
    )
    render_table(
        "Bot activity",
        [
            {
                "message": primary_snapshot.message,
                "signal": primary_snapshot.latest_signal.signal.value if primary_snapshot.latest_signal else "HOLD",
                "risk": primary_snapshot.latest_risk_decision.decision.value if primary_snapshot.latest_risk_decision else "-",
                "last_order": primary_snapshot.latest_execution_result.status if primary_snapshot.latest_execution_result else "-",
            }
        ],
    )


def _sync_multi_demo_runtimes(
    settings: BotSettings,
    symbols: list[str],
    interval: str,
    scenario: str,
    source: str,
    model_alias: str,
    max_daily_loss: Decimal,
    max_position: Decimal,
    max_trades: int,
    min_conf: float,
    max_spread: Decimal,
    max_data_age_ms: int,
    default_quote_size: Decimal,
    *,
    max_open_orders_per_symbol: int,
    demo_trading_armed: bool,
) -> None:
    current = st.session_state.get("multi_demo_runtimes", {})
    for old_symbol in list(current):
        if old_symbol not in symbols:
            current[old_symbol].stop()
            del current[old_symbol]
    for item in symbols:
        if item in current:
            continue
        current[item] = create_runtime(
            settings,
            "demo",
            item,
            interval,
            scenario,
            7,
            max_daily_loss,
            max_position,
            max_trades,
            min_conf,
            max_spread,
            source,
            model_alias,
            max_data_age_ms,
            default_quote_size,
            demo_trading_armed,
            max_demo_orders_per_session=max(10, max_trades),
            demo_pilot_preset="smoke",
        )
    st.session_state.multi_demo_runtimes = current


def _restart_completed_multi_runtime(
    settings: BotSettings,
    symbol: str,
    interval: str,
    scenario: str,
    source: str,
    model_alias: str,
    max_daily_loss: Decimal,
    max_position: Decimal,
    max_trades: int,
    min_conf: float,
    max_spread: Decimal,
    max_data_age_ms: int,
    default_quote_size: Decimal,
) -> None:
    cycles = st.session_state.get("multi_demo_cycles", {})
    cycles[symbol] = int(cycles.get(symbol, 0)) + 1
    st.session_state.multi_demo_cycles = cycles
    runtime = create_runtime(
        settings,
        "demo",
        symbol,
        interval,
        scenario,
        7 + cycles[symbol],
        max_daily_loss,
        max_position,
        max_trades,
        min_conf,
        max_spread,
        source,
        model_alias,
        max_data_age_ms,
        default_quote_size,
        True,
        max_demo_orders_per_session=max(10, max_trades),
        demo_pilot_preset="smoke",
    )
    try:
        runtime.start()
        st.session_state.multi_demo_runtimes[symbol] = runtime
    except (OSError, ValueError) as exc:
        st.session_state.simple_demo_error = str(exc)


def _multi_demo_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    cycles = st.session_state.get("multi_demo_cycles", {})
    for item, runtime in st.session_state.get("multi_demo_runtimes", {}).items():
        snapshot = runtime.snapshot()
        rows.append(
            {
                "symbol": item,
                "status": snapshot.status,
                "message": snapshot.message,
                "cycles": int(cycles.get(item, 0)),
                "signal": snapshot.latest_signal.signal.value if snapshot.latest_signal else "HOLD",
                "risk": snapshot.latest_risk_decision.decision.value if snapshot.latest_risk_decision else "-",
                "fills": len(snapshot.fills),
                "open_orders": len(snapshot.demo_open_orders),
                "equity": str(snapshot.equity),
            }
        )
    return rows


def _stop_one_multi_symbol(symbol: str) -> bool:
    target = symbol.strip().upper()
    if target and not target.endswith("USDT") and len(target) <= 6:
        target = f"{target}USDT"
    runtimes = st.session_state.get("multi_demo_runtimes", {})
    if not target or target not in runtimes:
        return False
    runtimes[target].stop()
    del runtimes[target]
    st.session_state.multi_demo_runtimes = runtimes
    if not runtimes:
        st.session_state.multi_demo_running = False
    return True


def _primary_multi_snapshot():
    runtimes = st.session_state.get("multi_demo_runtimes", {})
    if not runtimes:
        return None
    return next(iter(runtimes.values())).snapshot()


def _snapshot_for_symbol(symbol: str):
    runtime = st.session_state.get("multi_demo_runtimes", {}).get(symbol)
    return runtime.snapshot() if runtime else None


def _render_demo_spot_trading(settings: BotSettings, snapshot, symbol: str, interval: str) -> None:
    st.subheader("Demo Spot Trading")
    st.caption(f"{demo_trading_badge()} - Manual demo fills are local paper events only; no signed Binance order endpoint is called.")
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    col_a.metric("Mode", snapshot.mode)
    col_b.metric("Live", "disabled")
    col_c.metric("Manual fills", len(st.session_state.manual_demo_fills))
    col_d.metric("Base URL", settings.active_base_url)
    col_e.metric("Armed", "yes" if snapshot.demo_connection.get("armed") else "no")
    st.info(
        "Next safe action: "
        + (
            "use Demo Spot controls or start the Demo Pilot"
            if snapshot.demo_connection.get("armed")
            else "load/test Demo Spot credentials, then explicitly arm demo trading"
        )
    )
    if st.button("Refresh public Spot preview"):
        st.session_state.spot_preview = load_spot_symbol_preview(settings, symbol, interval, limit=60)
    preview: SpotPreview | None = st.session_state.get("spot_preview")
    if preview is None:
        st.info("Refresh the Spot preview before placing a local demo fill.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Source", preview.source)
        c2.metric("Last", f"{preview.last_price}")
        c3.metric("Spread bps", f"{preview.spread_bps}" if preview.spread_bps is not None else "-")
        c4.metric("Filter", preview.filters.status)
        render_debug(
            "Preview details",
            {
                "symbol": preview.symbol,
                "message": preview.message,
                "filters": {
                    "tick_size": str(preview.filters.tick_size),
                    "step_size": str(preview.filters.step_size),
                    "min_qty": str(preview.filters.min_qty),
                    "min_notional": str(preview.filters.min_notional),
                },
            }
        )
        with st.form("manual_demo_trade_form"):
            side = st.selectbox("Side", [OrderSide.BUY.value, OrderSide.SELL.value])
            quote_size = Decimal(str(st.number_input("Quote size", value=25.0, min_value=0.0, step=5.0)))
            quote_balance = Decimal(str(st.number_input("Paper quote balance", value=1000.0, min_value=0.0, step=50.0)))
            base_balance = Decimal(str(st.number_input("Paper base balance", value=0.0, min_value=0.0, step=0.001, format="%.6f")))
            confirmed = st.checkbox("I understand this is a local paper demo fill")
            submitted = st.form_submit_button("Create local demo fill")
        if submitted:
            request = ManualDemoTradeRequest(
                symbol=preview.symbol,
                side=OrderSide(side),
                quote_size=quote_size,
                price=preview.last_price,
                quote_balance=quote_balance,
                base_balance=base_balance,
                confirmed_demo_only=confirmed,
            )
            result = execute_manual_demo_trade(request, preview.filters)
            if result.fill:
                st.session_state.manual_demo_fills.append(result.fill)
                if snapshot.session_id:
                    SessionStore(settings.data_dir / "sessions").record_fill(snapshot.session_id, result.fill)
            render_debug("Trade result", {"status": result.status, "preview": result.preview.to_dict(), "fill": result.fill})
    if st.session_state.manual_demo_fills:
        render_table("Local demo fill history", st.session_state.manual_demo_fills[-10:])
    _render_demo_execution_drill(settings, snapshot, symbol)


def _render_demo_execution_drill(settings: BotSettings, snapshot, symbol: str) -> None:
    st.subheader("Demo Execution Drill")
    adapter = BinanceSpotAdapter(settings) if settings.binance_api_key and settings.binance_api_secret else None
    sandbox = DemoExecutionSandbox(settings, adapter=adapter)
    latest = sandbox.latest_report()
    render_badges(
        {
            "Profile": settings.exchange_profile,
            "Base URL": settings.active_base_url,
            "Credentials": "present" if settings.binance_api_key and settings.binance_api_secret else "missing",
            "Demo armed": "yes" if snapshot.demo_connection.get("armed") else "no",
            "Live": "disabled",
            "Kill switch": "on" if settings.kill_switch else "off",
            "Last drill": latest.get("status", "missing"),
        }
    )
    cols = st.columns(4)
    side = cols[0].selectbox("Drill side", [OrderSide.BUY.value, OrderSide.SELL.value], key="demo_execution_side")
    quote_size = cols[1].number_input("Drill quote size", min_value=0.0, value=10.0, step=5.0, key="demo_execution_quote_size")
    last_price = cols[2].number_input("Drill last price", min_value=0.000001, value=100.0, step=1.0, key="demo_execution_last_price")
    confirm_demo_order = cols[3].checkbox("Confirm demo order", key="demo_execution_confirm_order")
    action_cols = st.columns(6)
    intent = intent_from_values(symbol, side, str(quote_size), str(last_price))
    if action_cols[0].button("Preview order", key="demo_execution_preview", use_container_width=True):
        st.session_state.demo_execution_result = sandbox.preview(intent).to_dict()
    if action_cols[1].button("Test order only", key="demo_execution_test_order", use_container_width=True):
        st.session_state.demo_execution_result = sandbox.test_order_only(intent).to_dict()
    if action_cols[2].button("Place demo order", key="demo_execution_place_order", use_container_width=True):
        st.session_state.demo_execution_result = sandbox.place_demo_order(
            intent,
            confirm_demo_order=confirm_demo_order,
            armed=bool(snapshot.demo_connection.get("armed")),
        ).to_dict()
    query_client_id = st.text_input("Query client order id", value="", key="demo_execution_query_client_id")
    order_id = st.number_input("Cancel/query order id", min_value=0, value=0, step=1, key="demo_execution_order_id")
    confirm_cancel = st.checkbox("Confirm cancel", key="demo_execution_confirm_cancel")
    if action_cols[3].button("Query status", key="demo_execution_query", use_container_width=True):
        st.session_state.demo_execution_result = sandbox.query_order(
            symbol,
            order_id=int(order_id) or None,
            client_order_id=query_client_id or None,
        ).to_dict()
    if action_cols[4].button("Cancel order", key="demo_execution_cancel", use_container_width=True):
        st.session_state.demo_execution_result = sandbox.cancel_order(symbol, int(order_id), confirm_cancel=confirm_cancel).to_dict()
    if action_cols[5].button("Export drill evidence", key="demo_execution_export", use_container_width=True):
        st.session_state.demo_execution_result = latest
    result = st.session_state.get("demo_execution_result") or latest
    render_debug("Demo execution drill result", result)
    lifecycle = result.get("lifecycle", []) if isinstance(result, dict) else []
    render_table("Demo execution lifecycle", lifecycle if isinstance(lifecycle, list) else [])


def _render_credentials(manager: CredentialManager, settings: BotSettings, selected_profile: str, symbol: str) -> None:
    st.subheader("Credentials & Profile")
    profile = available_profiles()[selected_profile]
    st.metric("Mode badge", profile.mode_badge)
    st.write(f"REST base URL: `{settings.active_base_url}`")
    st.write(f"WebSocket base URL: `{profile.websocket_base_url}`")
    with st.form("credential_form"):
        api_key = st.text_input("API key", value="", type="password")
        api_secret = st.text_input("API secret", value="", type="password")
        use_session = st.form_submit_button("Use for this session")
    if use_session:
        manager.set_session_credentials(selected_profile, api_key, api_secret)
        st.success("Credentials loaded for this Streamlit session only.")
        st.rerun()
    cols = st.columns(4)
    if cols[0].button("Test connection"):
        checked = manager.apply_to_settings(settings, selected_profile)
        st.session_state.connectivity_report = connectivity_report(checked, symbol)
    if cols[1].button("Clear session credentials"):
        manager.clear()
        st.rerun()
    secret_store = WindowsSecretStoreAdapter()
    if cols[2].button("Save to Windows SecretStore"):
        if secret_store.is_available():
            st.warning("SecretStore is available, but write support is intentionally gated for a later confirmation flow.")
        else:
            st.warning(secret_store.docs_hint())
    render_debug("Credential status", manager.status().to_dict())
    if st.session_state.connectivity_report:
        st.subheader("Connectivity report")
        report = st.session_state.connectivity_report
        checks = {item["name"]: item["status"] for item in report.get("checks", [])}
        render_badges(
            {
                "Connection": report.get("status", "unknown"),
                "Base URL": report.get("base_url", "-"),
                "Account": checks.get("signed_account", "-"),
                "Server time": checks.get("server_time", "-"),
            }
        )
        render_debug("Connectivity report", report)


def _render_bot_controls(snapshot, running: bool, runtime_key: tuple) -> None:
    st.subheader("Bot Controls")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Running", "yes" if running else "no")
    b2.metric("Session", snapshot.session_id[-8:] if snapshot.session_id else "-")
    b3.metric("Fills", len(snapshot.fills))
    b4.metric("Blocks", sum(snapshot.metrics.block_reasons.values()))
    render_badges(
        {
            "Demo armed": str(snapshot.demo_connection.get("armed", False)),
            "Demo gate": snapshot.demo_connection.get("gate", {}).get("reason", "not-active"),
            "Live": "disabled",
        }
    )
    st.caption("Start, pause, step and emergency stop are in the sidebar.")
    render_debug("Active runtime key", {"active_runtime_key": [str(item) for item in runtime_key]})


def _render_strategy(snapshot, settings: BotSettings) -> None:
    st.subheader("Strategy & Model")
    render_debug("Active model", snapshot.active_model)
    st.subheader("Optional AI summary")
    if os.getenv("OPENAI_API_KEY"):
        st.info("AI summaries can be added with Structured Outputs. This panel is read-only and cannot generate orders.")
    else:
        st.warning("AI summaries disabled because OPENAI_API_KEY is not configured.")


def _render_market(snapshot) -> None:
    st.subheader("Market Data")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Bid", snapshot.top_of_book.get("bid", "-"))
    b2.metric("Ask", snapshot.top_of_book.get("ask", "-"))
    b3.metric("Mid", snapshot.top_of_book.get("mid_price", "-"))
    b4.metric("Spread bps", snapshot.top_of_book.get("spread_bps", "-"))
    render_debug("Market data details", snapshot.market_data)
    st.subheader("Data quality")
    render_debug("Data quality details", snapshot.data_quality)


def _render_orders(snapshot) -> None:
    st.subheader("Orders & Account")
    render_debug("User data stream", snapshot.user_data_stream)
    if snapshot.demo_account:
        render_debug("Demo account", snapshot.demo_account)
    if snapshot.demo_open_orders:
        render_table("Demo open orders", snapshot.demo_open_orders)
    render_table("Order lifecycle", snapshot.order_lifecycle)
    st.subheader("Testnet readiness")
    render_debug("Testnet readiness", snapshot.testnet_prechecks)


def _operator_snapshot_payload(snapshot) -> dict[str, object]:
    return asdict(snapshot)


def _render_demo_pilot(runtime, snapshot) -> None:
    st.subheader("Demo Pilot")
    operator_payload = _operator_snapshot_payload(snapshot)
    config = snapshot.demo_pilot.get("config", {})
    counters = snapshot.demo_pilot.get("counters", {})
    gate = snapshot.demo_connection.get("gate", {})
    pilot_status = runtime.pilot_orchestrator.status_payload(operator_payload)
    render_badges(
        {
            "Pilot": config.get("pilot_name", "-"),
            "Pilot state": pilot_status.get("state", "-"),
            "Run id": pilot_status.get("run_id", "-")[-12:] if pilot_status.get("run_id") else "-",
            "Armed": str(snapshot.demo_connection.get("armed", False)),
            "Status": snapshot.demo_pilot.get("status", "not-active"),
            "Resume required": str(snapshot.resume_required),
            "Base URL": snapshot.demo_connection.get("base_url", "-"),
            "Live": "disabled",
        }
    )
    if snapshot.resume_required or snapshot.reconciliation.get("needs_operator_action"):
        st.error("Operator action required: reconcile/cancel open demo orders before continuing.")
    elif not snapshot.demo_connection.get("armed"):
        st.warning("Next safe action: load Demo Spot credentials, test the connection, then explicitly arm demo trading.")
    else:
        st.success("Demo pilot is armed for Demo Spot only. Live trading remains disabled.")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Orders", counters.get("orders", 0))
    c2.metric("Max orders", config.get("max_demo_orders", "-"))
    c3.metric("Rejects", f"{counters.get('rejects', 0)} / {config.get('max_rejects', '-')}")
    c4.metric("API errors", f"{counters.get('api_errors', 0)} / {config.get('max_api_errors', '-')}")
    c5.metric("Reconcile fails", f"{counters.get('reconciliation_failures', 0)} / {config.get('max_reconciliation_failures', '-')}")
    c6.metric("Elapsed sec", counters.get("elapsed_seconds", 0))

    st.subheader("Pilot Run")
    gate_payload = pilot_status.get("gate", {})
    resume_payload = pilot_status.get("resume", {})
    start_action = pilot_status.get("start_action", {})
    latest_run = pilot_status.get("latest_run", {})
    pilot_run_state = str(latest_run.get("state") or pilot_status.get("state") or "idle")
    acceptance = pilot_status.get("acceptance", {})
    start_disabled = (
        bool(st.session_state.get("running"))
        or pilot_run_state in {"running", "stopping"}
        or bool(resume_payload.get("resume_required"))
        or not bool(gate_payload.get("allowed"))
    )
    recovery_action = "Resolve pilot recovery" if resume_payload.get("resume_required") or pilot_run_state == "resume_required" else "None"
    render_badges(
        {
            "Start gate": "ready" if gate_payload.get("allowed") else "blocked",
            "Next action": gate_payload.get("next_action", "-"),
            "Resume": "required" if resume_payload.get("resume_required") else "clean",
            "Runtime": snapshot.status,
            "Pilot run": pilot_run_state,
            "Start action": start_action.get("next_action", "Start Demo Spot pilot"),
            "Recovery action": recovery_action,
            "Open orders": resume_payload.get("open_orders", 0),
            "Recon age ms": snapshot.demo_pilot.get("last_reconciliation_check_ms", 0),
            "Account sync ms": snapshot.demo_pilot.get("last_demo_account_sync_ms", 0),
        }
    )
    render_table("Start gate", gate_payload.get("checks", []))
    render_table("Acceptance criteria", [acceptance])
    run_cols = st.columns(3)
    if pilot_run_state == "running":
        st.info("Pilot is already running. Use Safe stop pilot before starting another run.")
    elif start_disabled:
        st.caption(start_action.get("next_action") or gate_payload.get("next_action") or "Resolve start blockers before starting.")
    if run_cols[0].button("Start Demo Spot Pilot", use_container_width=True, disabled=start_disabled):
        gate_now = runtime.pilot_orchestrator.evaluate_start_gate(operator_payload)
        if gate_now.get("allowed"):
            try:
                runtime.start()
                st.session_state.running = True
            except ValueError as exc:
                st.session_state.demo_pilot_hint = f"Pilot start blocked: {exc}"
        else:
            st.session_state.demo_pilot_hint = gate_now.get("next_action", "Resolve start blockers")
        st.rerun()
    if run_cols[1].button("Safe stop pilot", use_container_width=True):
        runtime.stop()
        st.session_state.running = False
        st.session_state.demo_report_paths = runtime.report_paths
        st.rerun()
    if run_cols[2].button("Mark resolved", use_container_width=True):
        record = runtime.pilot_orchestrator.mark_resolved(operator_payload)
        st.session_state.demo_pilot_hint = "Resolved" if record and record.state == "completed" else "Blockers remain"
        st.rerun()

    st.subheader("Runner Mission Control")
    runner_service = PilotRunnerService(BotSettings.from_env())
    runner_status = runner_service.status()
    runner = runner_status.get("runner", {})
    runner_health = runner_status.get("runner_health", {})
    telemetry_summary = runner_status.get("telemetry_summary", {})
    stale_recovery = runner_status.get("stale_recovery", {})
    telemetry_rows = runner_status.get("telemetry_rows", [])
    runner_commands = runner_status.get("commands", [])
    render_badges(
        {
            "Runner": runner.get("state", "not_running"),
            "Alive": str(runner.get("alive", False)),
            "Stale": str(runner.get("stale", False)),
            "Heartbeat age ms": runner.get("heartbeat_age_ms", 0),
            "PID": runner.get("pid", "-"),
            "Next action": runner_health.get("next_safe_action", runner.get("next_action", "-")),
            "Failed cmds": runner_health.get("failed_commands", 0),
            "Telemetry rows": runner_health.get("telemetry_rows", 0),
        }
    )
    render_table("Runner health", [runner_health])
    render_table("Telemetry summary", [telemetry_summary])
    render_table(
        "Operator link status",
        [
            {
                "demo_armed": snapshot.demo_connection.get("armed", False),
                "runner_alive": runner.get("alive", False),
                "runner_stale": runner.get("stale", False),
                "heartbeat_age_ms": runner.get("heartbeat_age_ms", 0),
                "command_queue": len(runner_commands),
                "next_safe_action": runner_health.get("next_safe_action", runner.get("next_action", "-")),
            }
        ],
    )
    chart_a, chart_b = st.columns(2)
    with chart_a:
        render_plotly_chart(runner_heartbeat_figure(telemetry_rows), key=DEMO_PILOT_HEARTBEAT)
        render_plotly_chart(runner_counters_figure(telemetry_rows), key=DEMO_PILOT_COUNTERS)
    with chart_b:
        render_plotly_chart(runner_equity_pnl_figure(telemetry_rows), key=DEMO_PILOT_EQUITY_PNL)
        render_plotly_chart(command_status_figure(runner_commands), key=DEMO_PILOT_COMMAND_STATUS)
    if stale_recovery.get("stale"):
        st.warning("Runner stale: follow recovery steps before starting a new pilot.")
    render_table("Stale recovery", stale_recovery.get("steps", []))
    runner_cols = st.columns(6)
    if runner_cols[0].button("Start runner", use_container_width=True):
        st.session_state.runner_start_result = start_background_runner(
            symbol=snapshot.symbol,
            interval=snapshot.interval,
            preset=config.get("pilot_name", "smoke"),
            source="demo",
            cwd=Path.cwd(),
        )
        st.rerun()
    confirm_stop_runner = st.checkbox("Confirm stop runner")
    confirm_cancel_runner = st.checkbox("Confirm runner cancel open orders")
    confirm_clear_stale = st.checkbox("Confirm clear stale lock")
    if runner_cols[1].button("Stop runner", use_container_width=True):
        if not confirm_stop_runner:
            st.session_state.runner_command = {"status": "blocked", "reason": "confirm stop runner first"}
            st.rerun()
        st.session_state.runner_command = runner_service.enqueue_command("stop")
        st.rerun()
    if runner_cols[2].button("Runner reconcile", use_container_width=True):
        st.session_state.runner_command = runner_service.enqueue_command("reconcile")
        st.rerun()
    if runner_cols[3].button("Runner cancel", use_container_width=True):
        if not confirm_cancel_runner:
            st.session_state.runner_command = {"status": "blocked", "reason": "confirm runner cancel first"}
            st.rerun()
        st.session_state.runner_command = runner_service.enqueue_command("cancel_open_orders")
        st.rerun()
    if runner_cols[4].button("Runner export", use_container_width=True):
        st.session_state.runner_command = runner_service.enqueue_command("export_report")
        st.rerun()
    if runner_cols[5].button("Clear stale lock", use_container_width=True):
        if not confirm_clear_stale:
            st.session_state.runner_clear_stale = {"status": "blocked", "reason": "confirm clear stale lock first"}
            st.rerun()
        st.session_state.runner_clear_stale = runner_service.clear_stale_lock()
        st.rerun()
    if st.session_state.get("runner_start_result"):
        render_debug("Runner start", st.session_state.runner_start_result)
    if st.session_state.get("runner_command"):
        render_debug("Runner command", st.session_state.runner_command)
    render_table("Runner telemetry", [runner_status.get("latest_telemetry", {})] if runner_status.get("latest_telemetry") else [])
    render_table("Runner commands", runner_commands)
    report_paths = runner_status.get("latest_run", {}).get("report_paths", {})
    runner_paths = {
        "command_dir": runner.get("command_dir", ""),
        "telemetry_jsonl": runner.get("telemetry_jsonl", ""),
        "latest_telemetry_json": runner.get("latest_telemetry_json", ""),
        **{f"report_{key}": value for key, value in report_paths.items()},
    }
    render_table("Runner paths", [{"artifact": key, "path": value} for key, value in runner_paths.items() if value])

    cols = st.columns(8)
    if cols[0].button("Connect", use_container_width=True):
        st.session_state.demo_pilot_hint = "Open Credentials & Profile, load Demo Spot keys, then use Test connection."
    if cols[1].button("Test connection", use_container_width=True):
        st.session_state.demo_pilot_hint = gate.get("reason", "Credentials are evaluated on runtime reset/connection checks.")
    if cols[2].button("Reconcile now", use_container_width=True):
        st.session_state.demo_reconciliation = runtime.reconcile_demo_orders()
        st.rerun()
    if cols[3].button("Arm", use_container_width=True):
        st.session_state.demo_trading_armed = True
        st.session_state.runtime_key = None
        st.rerun()
    if cols[4].button("Disarm", use_container_width=True):
        st.session_state.demo_trading_armed = False
        st.session_state.runtime_key = None
        st.rerun()
    if cols[5].button("Stop", use_container_width=True):
        runtime.stop()
        st.session_state.running = False
        st.rerun()
    if cols[6].button("Cancel open orders", use_container_width=True):
        st.session_state.demo_cancel_status = runtime.cancel_demo_open_orders()
        st.rerun()
    if cols[7].button("Export report", use_container_width=True):
        runtime.stop()
        st.session_state.demo_report_paths = runtime.report_paths
        st.rerun()
    if st.button("Reset local runtime", use_container_width=True):
        st.session_state.runtime_key = None
        st.rerun()
    if st.session_state.get("demo_pilot_hint"):
        st.info(st.session_state.demo_pilot_hint)

    render_table("Operator checklist", operator_checklist(operator_payload))
    render_table(
        "Pilot preset",
        [
            {
                "name": config.get("pilot_name", "-"),
                "duration_min": config.get("duration_minutes", "-"),
                "max_orders": config.get("max_demo_orders", "-"),
                "max_rejects": config.get("max_rejects", "-"),
                "max_api_errors": config.get("max_api_errors", "-"),
                "max_reconcile_failures": config.get("max_reconciliation_failures", "-"),
                "cancel_on_stop": config.get("cancel_open_orders_on_stop", "-"),
                "pause_reason": snapshot.demo_pilot.get("pause_reason", ""),
            }
        ],
    )
    render_table("Signal to order pipeline", pipeline_rows(operator_payload))
    render_table("Open demo orders", snapshot.demo_open_orders)
    render_table("Order lifecycle", snapshot.order_lifecycle)
    if snapshot.demo_order_errors:
        render_table("Demo order errors", snapshot.demo_order_errors)
    if snapshot.cancel_on_stop_status or st.session_state.get("demo_cancel_status"):
        render_table("Cancel status", snapshot.cancel_on_stop_status or st.session_state.demo_cancel_status)
    if st.session_state.get("demo_report_paths"):
        render_table("Pilot report paths", [{"artifact": key, "path": value} for key, value in st.session_state.demo_report_paths.items()])
    with st.expander("Technical payloads"):
        render_debug("Reconciliation", snapshot.reconciliation)
        render_debug("Demo account", snapshot.demo_account)


def _render_sessions(snapshot) -> None:
    st.subheader("Sessions")
    st.write(f"Current session: `{snapshot.session_id}`")
    render_table("Recent sessions", snapshot.recent_sessions)
    store = SessionStore(BotSettings.from_env().data_dir / "sessions")
    session_ids = [item.get("session_id", "") for item in snapshot.recent_sessions if item.get("session_id")]
    if session_ids:
        selected = st.selectbox("Replay session", session_ids)
        frames = ReplaySandbox(store).chart_points(selected)
        render_table("Replay timeline", frames[:100])
        compare_ids = st.multiselect("Compare sessions", session_ids, default=session_ids[:2] if len(session_ids) >= 2 else [])
        if len(compare_ids) >= 2:
            render_table("Session comparison", [row.to_dict() for row in compare_sessions(store, compare_ids[:10])])
    st.download_button(
        "Export current session summary",
        data=json.dumps(snapshot.session_summary, default=str, indent=2),
        file_name=f"{snapshot.session_id}-summary.json",
        mime="application/json",
    )


def _render_evaluation(snapshot, settings: BotSettings, symbol: str, interval: str) -> None:
    st.subheader("Model Lab")
    col_a, col_b = st.columns(2)
    with col_a:
        run_baseline = st.button("Run baseline evaluation", use_container_width=True)
    with col_b:
        run_walk_forward = st.button("Run walk-forward evaluation", use_container_width=True)
    if run_baseline or run_walk_forward:
        if len(snapshot.candles) > 20:
            report = (
                evaluate_walk_forward(symbol, interval, snapshot.candles)
                if run_walk_forward
                else evaluate_rule_baseline(symbol, interval, snapshot.candles)
            )
            st.session_state.evaluation_report = report_to_dict(report)
        else:
            st.warning("Run the bot for more candles before evaluation.")
    if st.session_state.evaluation_report:
        report = st.session_state.evaluation_report
        render_badges(
            {
                "Mode": report.get("mode", "evaluation"),
                "Folds": len(report.get("folds", [])),
                "Leakage": report.get("leakage", {}).get("status", "not-run"),
                "Live": "disabled",
            }
        )
        if report.get("candidate_summary"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Candidate pnl", report["candidate_summary"].get("pnl", "0"))
            c2.metric("Baseline pnl", report["baseline_summary"].get("pnl", "0"))
            c3.metric("Beats baseline", str(report["candidate_summary"].get("beats_baseline", False)))
        if report.get("manifest"):
            manifest = report["manifest"]
            render_debug(
                "Dataset manifest",
                {
                    "dataset_id": manifest.get("dataset_id"),
                    "feature_schema_hash": manifest.get("feature_schema_hash"),
                    "label_horizon": manifest.get("label_horizon"),
                    "row_count": manifest.get("row_count"),
                    "checksum": manifest.get("checksum"),
                },
            )
        render_table("Walk-forward folds", report.get("folds", []))
        with st.expander("Raw evaluation report"):
            st.json(report)
    else:
        st.caption("Run after enough candles are available.")
    registry = ModelRegistry(settings.data_dir / "models")
    models = registry.list_models()
    if models:
        st.subheader("Model registry gates")
        rows = []
        for model in models:
            decision = registry.evaluate_promotion(model, operator_confirmed=False)
            rows.append(
                {
                    "model_id": model.model_id,
                    "role": model.role,
                    "dataset_id": model.dataset_id,
                    "schema": model.feature_schema_hash,
                    "promotion_blockers": ", ".join(decision.reasons),
                    "shadow_only": model.role in {"candidate", "shadow"},
                }
            )
        render_table("Registered models", rows)
    else:
        st.caption("No registered models yet.")


def _render_strategy_lab(snapshot) -> None:
    st.subheader("Strategy Lab")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("Risk decision debugger")
        if snapshot.latest_risk_decision:
            render_table("Latest risk decision", [explain_decision(snapshot.latest_risk_decision).to_dict()])
        else:
            st.caption("No risk decision yet.")
        render_table("Risk timeline", [event.to_dict() for event in timeline_from_events(snapshot.audit_tail)])
    with col_b:
        st.write("Signal explanation")
        if snapshot.latest_signal and snapshot.current_candle:
            row = FeatureRow(
                snapshot.symbol,
                snapshot.current_candle.close_time_ms,
                {"close": float(snapshot.current_candle.close), "confidence": float(snapshot.latest_signal.confidence)},
                snapshot.current_candle.close,
            )
            explanation = explain_signal(snapshot.latest_signal, row).to_dict()
            render_badges(
                {
                    "Signal": explanation["signal"],
                    "Confidence": round(explanation["confidence"], 4),
                    "Horizon": explanation["horizon"],
                    "Model": explanation["model_version"],
                }
            )
            render_table("Top features", [{"feature": key, "value": value} for key, value in explanation["top_features"]])
        else:
            st.caption("Run or step the bot to inspect a signal.")
        st.write("Strategy templates")
        render_table("Templates", list_strategy_templates())


def _render_research(snapshot, settings: BotSettings) -> None:
    st.subheader("Research")
    spread = float(snapshot.top_of_book.get("spread_bps") or 0)
    confidence = float(snapshot.latest_signal.confidence) if snapshot.latest_signal else 0.0
    signal = snapshot.latest_signal.signal.value if snapshot.latest_signal else "HOLD"
    scanner_rows = rank_watchlist([ScannerRow(snapshot.symbol, spread, 0.0, signal, confidence)])
    render_table("Scanner ranking", [row.to_dict() for row in scanner_rows])
    experiments = ExperimentDB(settings.data_dir / "experiments" / "experiments.json")
    history = ScannerHistory(settings.data_dir / "scanner" / "history.jsonl", experiments)
    if st.button("Record scanner run"):
        st.session_state.scanner_run = history.record_run(scanner_rows)
    if st.button("Export scanner reports"):
        payload = {"rows": [row.to_dict() for row in scanner_rows], "orders_allowed": False}
        html_path = export_html_report("Scanner Research", payload, settings.data_dir / "reports" / "scanner.html")
        notebook_path = export_notebook("Scanner Research", payload, settings.data_dir / "reports" / "scanner.ipynb")
        st.session_state.scanner_exports = {"html": str(html_path), "notebook": str(notebook_path)}
    render_table("Scanner history", history.list_runs()[-10:])
    if st.session_state.get("scanner_exports"):
        render_debug("Scanner exports", st.session_state.scanner_exports)
    manifest = cache_manifest(settings.data_dir)
    render_badges({"Cache entries": len(manifest["entries"]), "Manifest time": manifest["created_at_ms"]})


def _render_portfolio(snapshot) -> None:
    st.subheader("Portfolio")
    portfolio = Portfolio()
    portfolio.set_balance("USDT", Decimal(str(snapshot.paper_quote)))
    mark = Decimal(str(snapshot.current_candle.close)) if snapshot.current_candle else Decimal("0")
    if snapshot.paper_position > 0:
        portfolio.positions[snapshot.symbol] = portfolio.positions.get(snapshot.symbol) or Position(snapshot.symbol, snapshot.paper_position, mark)
    render_badges(
        {
            "Quote": portfolio.to_dict()["balances"].get("USDT", "0"),
            "Total equity": str(portfolio.total_equity({snapshot.symbol: mark})),
            "Exposure": str(portfolio.total_exposure({snapshot.symbol: mark})),
            "Fees": snapshot.paper_account.get("fees_paid", "0"),
        }
    )
    render_table("Positions", list(portfolio.to_dict()["positions"].values()))


def _render_readiness(snapshot) -> None:
    st.subheader("Readiness")
    evidence = {"check-all", "secret-scan"}
    if snapshot.session_id:
        evidence.add("paper-report")
    score = score_readiness(evidence)
    render_badges({"Readiness": score.level, "Live allowed": str(score.live_allowed), "Blockers": len(score.blockers)})
    render_table("Readiness blockers", [{"blocker": item} for item in score.blockers])
    st.write("Copilot guard")
    render_table("Copilot permissions", [check_copilot_action(action).to_dict() for action in ["summarize_session", "place_order", "enable_live", "read_api_secret"]])
    st.write("Chaos scenarios")
    render_table("Chaos scenarios", [simulate_failure(key).to_dict() for key in ["429", "418", "5xx", "websocket_disconnect", "stale_data", "write_failure", "unknown_order"]])
    guard = TestnetEnduranceGuard(max_orders=5)
    render_debug("Testnet endurance guard", guard.to_dict())
    profiles = available_profiles()
    render_table(
        "Profile readiness",
        [
            {
                "profile": item.name,
                "mode": item.trading_mode.value,
                "requires_credentials": item.requires_credentials,
                "live_disabled": True,
                "base_url": item.rest_base_url,
            }
            for item in profiles.values()
        ],
    )
    if st.button("Record readiness evidence"):
        vault = EvidenceVault(BotSettings.from_env().data_dir / "evidence" / "evidence.jsonl")
        evidence_record = vault.add("readiness-score", score.to_dict())
        st.session_state.readiness_evidence = evidence_record.to_dict()
    if st.session_state.get("readiness_evidence"):
        render_debug("Readiness evidence", st.session_state.readiness_evidence)
    st.subheader("Evidence Scorecard")
    settings = BotSettings.from_env()
    if st.button("Generate scorecard", key="evidence_scorecard_generate", use_container_width=True):
        scorecard = generate_evidence_scorecard(settings, write=False)
        path = write_scorecard(settings, scorecard)
        st.session_state.evidence_scorecard = {"path": str(path), **scorecard.to_dict()}
    scorecard_payload = st.session_state.get("evidence_scorecard")
    if not scorecard_payload:
        scorecard = generate_evidence_scorecard(settings, write=False)
        scorecard_payload = scorecard.to_dict()
    render_badges(
        {
            "Overall": scorecard_payload.get("status", "unknown"),
            "Blockers": len(scorecard_payload.get("blockers", [])),
            "Warnings": len(scorecard_payload.get("warnings", [])),
            "Live": "disabled",
            "Browser smoke": "ok"
            if "browser_smoke" in scorecard_payload.get("artifacts", {})
            else "missing",
            "Demo execution": "present"
            if "demo_execution" in scorecard_payload.get("artifacts", {})
            else "missing",
        }
    )
    st.info(f"Next safe action: {scorecard_payload.get('next_safe_action', '-')}")
    render_table("Evidence scorecard blockers", scorecard_payload.get("blockers", []))
    render_table("Evidence scorecard warnings", scorecard_payload.get("warnings", []))
    render_debug("Evidence scorecard details", scorecard_payload)
    st.subheader("Demo Acceptance Rehearsal")
    browser_url = st.text_input("Rehearsal browser URL", value="", key="rehearsal_browser_url")
    if st.button("Run rehearsal", key="demo_acceptance_rehearsal_run", use_container_width=True):
        st.session_state.demo_acceptance_rehearsal = DemoAcceptanceRehearsal(settings, Path.cwd()).run(
            browser_url=browser_url
        ).to_dict()
    history = RehearsalHistory(settings.data_dir)
    latest_rehearsal = st.session_state.get("demo_acceptance_rehearsal") or history.latest()
    recent_rehearsals = history.list_recent(10)
    trend_points = history.trend_points(20)
    if latest_rehearsal:
        render_badges(
            {
                "Latest": latest_rehearsal.get("status", "unknown"),
                "Scorecard": latest_rehearsal.get("scorecard_status", "unknown"),
                "Blockers": len(latest_rehearsal.get("blockers", [])),
                "Warnings": len(latest_rehearsal.get("warnings", [])),
                "Duration": latest_rehearsal.get("duration_seconds", 0),
                "Artifacts": len(latest_rehearsal.get("artifacts", {})),
            }
        )
        render_table("Rehearsal steps", latest_rehearsal.get("steps", []))
        render_table("Rehearsal blockers", latest_rehearsal.get("blockers", []))
        render_table("Rehearsal warnings", latest_rehearsal.get("warnings", []))
    render_table("Recent rehearsals", recent_rehearsals)
    render_table("Rehearsal trend", trend_points)
    st.subheader("Recovery & Diagnostics")
    diagnostics_payload = st.session_state.get("operator_diagnostics")
    if st.button("Refresh diagnostics", key="operator_diagnostics_refresh", use_container_width=True):
        diagnostics_payload = collect_diagnostics(settings).to_dict()
        st.session_state.operator_diagnostics = diagnostics_payload
    if not diagnostics_payload:
        diagnostics_payload = collect_diagnostics(settings).to_dict()
    diag_cols = st.columns(2)
    if diag_cols[0].button("Run diagnostics rehearsal", key="operator_diagnostics_rehearsal", use_container_width=True):
        st.session_state.demo_acceptance_rehearsal = DemoAcceptanceRehearsal(settings, Path.cwd()).run(
            browser_url=browser_url
        ).to_dict()
        st.session_state.operator_diagnostics = collect_diagnostics(settings).to_dict()
        st.rerun()
    if diag_cols[1].button("Export support bundle", key="operator_diagnostics_support_bundle", use_container_width=True):
        st.session_state.support_bundle = create_support_bundle(
            settings, settings.data_dir / "support" / "support-bundle.zip"
        )
    render_badges(
        {
            "Overall health": diagnostics_payload.get("status", "unknown"),
            "Pilot run": (diagnostics_payload.get("pilot_run_health") or {}).get("state", "unknown"),
            "Runner lock": (diagnostics_payload.get("runner_lock_health") or {}).get("state", "unknown"),
            "Latest rehearsal": latest_rehearsal.get("status", "missing") if latest_rehearsal else "missing",
            "Latest scorecard": scorecard_payload.get("status", "unknown"),
            "Live": "disabled",
        }
    )
    st.info(f"Diagnostics next safe action: {diagnostics_payload.get('next_safe_action', '-')}")
    render_table("Diagnostics blockers", diagnostics_payload.get("blockers", []))
    render_table("Diagnostics warnings", diagnostics_payload.get("warnings", []))
    render_table("Recommended actions", diagnostics_payload.get("recommended_actions", []))
    render_table("Artifact inventory", diagnostics_payload.get("artifact_inventory", []))
    render_table("Diagnostics retention preview", retention_preview(settings).get("items", []))
    render_table("Operator incident timeline", incident_timeline(settings, limit=20))
    health_score = operator_health_score(settings)
    render_badges(
        {
            "Operator health score": health_score.get("score", 0),
            "Health grade": health_score.get("grade", "unknown"),
            "Next best action": health_score.get("next_best_action", "-"),
            "Live trading": "disabled",
        }
    )
    render_table("Operator action priority engine", health_score.get("priorities", []))
    render_debug("Operator health severity counts", health_score.get("severity_counts", {}))
    catalog = artifact_catalog(settings)
    render_badges(
        {
            "Artifact catalog files": catalog.get("count", 0),
            "Stale artifacts": catalog.get("summaries", {}).get("stale_count", 0),
            "Catalog groups": len(catalog.get("summaries", {}).get("by_category", {})),
        }
    )
    render_table("Local artifact catalog", catalog.get("artifacts", [])[:20])
    render_debug("Artifact catalog filters and staleness groups", catalog.get("summaries", {}))
    render_table("Rehearsal profiles fast standard deep", rehearsal_profiles().get("profiles", []))
    render_debug("Operator report diff last two runs", operator_report_diff(settings))
    render_debug("Evidence integrity chain hashes", evidence_chain(settings))
    render_table("Environment doctor Python deps paths", environment_doctor(settings).get("checks", []))
    render_debug("Data growth budget forecast", data_growth_budget(settings))
    render_table(
        "Local Ops Command Palette",
        [
            {"command": item.get("command"), "purpose": item.get("purpose")}
            for item in operator_command_manifest().get("commands", [])
        ],
    )
    render_debug("Diagnostics baseline drift", diagnostics_baseline(settings))
    render_table("Operator report index", report_index(settings).get("reports", []))
    render_table("Support bundle verification matrix", verify_support_bundles(settings).get("bundles", []))
    render_debug("Redaction self-test", redaction_self_test())
    render_table("Operator command manifest", operator_command_manifest().get("commands", []))
    render_debug("Local ops snapshot", local_ops_snapshot(settings))
    if st.button("Export operator report", key="operator_report_export", use_container_width=True):
        st.session_state.operator_report = export_operator_report(settings)
    if st.session_state.get("operator_report"):
        render_debug("Operator report", st.session_state.operator_report)
    if st.session_state.get("support_bundle"):
        render_debug("Support bundle", st.session_state.support_bundle)
    st.info("Live-readiness remains design-only; live trading is not enabled from this dashboard.")


def _render_logs_security(snapshot, settings: BotSettings) -> None:
    st.subheader("Logs & Security")
    if st.button("Run preflight checks"):
        st.session_state.preflight_report = run_preflight(settings).to_dict()
    if st.session_state.get("preflight_report"):
        st.subheader("Preflight")
        render_debug("Preflight details", st.session_state.preflight_report)
    if st.button("Collect diagnostics"):
        st.session_state.diagnostics_report = collect_diagnostics(settings).to_dict()
    if st.session_state.get("diagnostics_report"):
        st.subheader("Diagnostics")
        render_debug("Diagnostics details", st.session_state.diagnostics_report)
    render_alert_list(snapshot.alerts[-20:])
    render_debug(
        "Security details",
        {
            "live_trading_enabled": settings.live_trading_enabled,
            "kill_switch": settings.kill_switch,
            "audit_tail": snapshot.audit_tail[-8:],
            "block_reasons": snapshot.metrics.block_reasons,
            "secret_policy": "session-only by default; no plaintext secrets are written to repo, logs, audit or sessions",
        }
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import sys
import time
from decimal import Decimal
from pathlib import Path

from .audit import AuditLog
from .backtest import BacktestEngine
from .action_center import create_reviewed_action
from .binance_data_ingestion import BinanceDataIngestionService, IngestionRequest, export_public_data_evidence
from .config import BotSettings
from .connectivity import connectivity_report
from .check_all import payload_for, print_payload, run_checks
from .control_center import start_control_center
from .data import DataStore, parse_binance_klines
from .data_quality import check_candles
from .demo import DemoMarketReplay
from .disaster_recovery_drills import run_disaster_recovery_drill
from .diagnostics import collect_diagnostics
from .evaluation import WalkForwardConfig, evaluate_rule_baseline, evaluate_walk_forward, report_to_dict
from .experiment_db import ExperimentDB
from .features import build_feature_rows, build_label_rows
from .indicator_warmup import warmup_indicators
from .launcher import find_free_port
from .local_ops_automation import generate_scheduled_ops_report
from .metrics_warehouse import write_metrics_report
from .model_registry import ModelRegistry
from .operator_ops import (
    artifact_catalog,
    create_state_archive,
    data_growth_budget,
    diagnostics_baseline,
    environment_doctor,
    evidence_chain,
    export_operator_report,
    incident_timeline,
    local_ops_snapshot,
    operator_command_manifest,
    operator_health_score,
    operator_quality_gate,
    operator_report_diff,
    redaction_self_test,
    rehearsal_profiles,
    report_index,
    retention_preview,
    support_bundle_restore_preview,
    verify_support_bundles,
    write_evidence_manifest,
    write_timeline_markdown,
)
from .paper_deployment import run_paper_deployment_cycle
from .paper_portfolio_ops import PaperStrategy, run_portfolio_operations
from .permission_profiles import evaluate_permission, permission_compliance_report
from .policy_rollout import run_policy_rollout
from .portfolio_benchmarking import benchmark_allocations, write_benchmark_report
from .portfolio_optimization import optimize_portfolio_policy
from .portfolio_policy_registry import PortfolioPolicyRegistry, demo_policy
from .policy_promotion_gate import evaluate_policy_promotion
from .paper_policy_rollout import create_rollout_plan
from .ab_paper_experiments import run_ab_paper_experiment, write_ab_experiment_report
from .experiment_stopping_rules import evaluate_stopping_rules
from .policy_governance import governance_decision
from .weekly_governance_report import write_weekly_governance_report
from .policy_lineage import rollback_to_previous_champion
from .governance_evidence_bundle import export_governance_evidence_bundle
from .governance_simulation import run_governance_simulation
from .pilot_orchestrator import DemoPilotOrchestrator, PilotRunStore
from .pilot_runner import PilotRunnerService, start_background_runner
from .preflight import run_preflight
from .risk import RiskEngine, RiskLimits
from .runtime import BotRuntime, RuntimeOptions, snapshot_to_dict
from .security import scan_for_secrets
from .session_report import export_session_report
from .session_store import SessionStore
from .signal_model import TinyNeuralSignalModel
from .ops_assistant import write_ops_assistant_answer
from .strategy_calibration import calibrate_strategy
from .support_bundle import create_support_bundle, verify_support_bundle


def main() -> None:
    parser = argparse.ArgumentParser(prog="spot-bot")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate-config")
    sub.add_parser("preflight")
    diagnostics = sub.add_parser("diagnostics")
    diagnostics.add_argument("--json", action="store_true")
    diagnostics.add_argument("--strict", action="store_true")
    support_bundle = sub.add_parser("support-bundle")
    support_bundle.add_argument("--output", default="")
    support_bundle.add_argument("--json", action="store_true")
    support_verify = sub.add_parser("support-bundle-verify")
    support_verify.add_argument("--bundle", required=True)
    support_verify.add_argument("--json", action="store_true")
    retention = sub.add_parser("retention-preview")
    retention.add_argument("--older-than-days", type=int, default=7)
    retention.add_argument("--json", action="store_true")
    archive_state = sub.add_parser("state-archive")
    archive_state.add_argument("--output", default="")
    archive_state.add_argument("--older-than-days", type=int, default=7)
    archive_state.add_argument("--json", action="store_true")
    timeline = sub.add_parser("incident-timeline")
    timeline.add_argument("--markdown", action="store_true")
    timeline.add_argument("--json", action="store_true")
    operator_report = sub.add_parser("operator-report")
    operator_report.add_argument("--json", action="store_true")
    quality_gate = sub.add_parser("operator-quality-gate")
    quality_gate.add_argument("--json", action="store_true")
    quality_gate.add_argument("--strict", action="store_true")
    artifact_catalog_parser = sub.add_parser("artifact-catalog")
    artifact_catalog_parser.add_argument("--category", default="")
    artifact_catalog_parser.add_argument("--suffix", default="")
    artifact_catalog_parser.add_argument("--stale-days", type=int, default=7)
    artifact_catalog_parser.add_argument("--json", action="store_true")
    health_score = sub.add_parser("operator-health-score")
    health_score.add_argument("--json", action="store_true")
    profiles_parser = sub.add_parser("rehearsal-profiles")
    profiles_parser.add_argument("--json", action="store_true")
    report_diff_parser = sub.add_parser("operator-report-diff")
    report_diff_parser.add_argument("--json", action="store_true")
    restore_preview_parser = sub.add_parser("support-bundle-restore-preview")
    restore_preview_parser.add_argument("--bundle", required=True)
    restore_preview_parser.add_argument("--json", action="store_true")
    evidence_chain_parser = sub.add_parser("evidence-chain")
    evidence_chain_parser.add_argument("--json", action="store_true")
    environment_doctor_parser = sub.add_parser("environment-doctor")
    environment_doctor_parser.add_argument("--json", action="store_true")
    data_growth_parser = sub.add_parser("data-growth-budget")
    data_growth_parser.add_argument("--budget-bytes", type=int, default=100_000_000)
    data_growth_parser.add_argument("--json", action="store_true")
    baseline = sub.add_parser("diagnostics-baseline")
    baseline.add_argument("--write", action="store_true")
    baseline.add_argument("--json", action="store_true")
    report_index_parser = sub.add_parser("report-index")
    report_index_parser.add_argument("--json", action="store_true")
    support_bundles_verify = sub.add_parser("support-bundles-verify")
    support_bundles_verify.add_argument("--json", action="store_true")
    redaction_parser = sub.add_parser("redaction-self-test")
    redaction_parser.add_argument("--json", action="store_true")
    snapshot_parser = sub.add_parser("local-ops-snapshot")
    snapshot_parser.add_argument("--json", action="store_true")
    command_manifest_parser = sub.add_parser("operator-command-manifest")
    command_manifest_parser.add_argument("--json", action="store_true")
    evidence_manifest_parser = sub.add_parser("evidence-manifest")
    evidence_manifest_parser.add_argument("--json", action="store_true")
    fetch_public = sub.add_parser("fetch-public-data")
    fetch_public.add_argument("--symbols", default="BTCUSDT,ETHUSDT,BNBUSDT")
    fetch_public.add_argument("--intervals", default="1m,5m,15m,1h")
    fetch_public.add_argument("--limit", type=int, default=120)
    fetch_public.add_argument("--json", action="store_true")
    warmup_public = sub.add_parser("warmup-indicators")
    warmup_public.add_argument("--symbols", default="BTCUSDT,ETHUSDT,BNBUSDT")
    warmup_public.add_argument("--limit", type=int, default=120)
    warmup_public.add_argument("--json", action="store_true")
    sub.add_parser("public-data-status")
    clear_public = sub.add_parser("clear-public-data-cache")
    clear_public.add_argument("--confirm", default="")
    public_evidence = sub.add_parser("public-data-evidence")
    public_evidence.add_argument("--json", action="store_true")
    strategy_calibrate = sub.add_parser("strategy-calibrate")
    strategy_calibrate.add_argument("--symbols", default="BTCUSDT,ETHUSDT,BNBUSDT")
    strategy_calibrate.add_argument("--interval", default="1m")
    strategy_calibrate.add_argument("--scenario", default="sideways")
    strategy_calibrate.add_argument("--json", action="store_true")
    paper_deploy = sub.add_parser("paper-deployment-cycle")
    paper_deploy.add_argument("--strategy-id", default="adaptive-indicator")
    paper_deploy.add_argument("--model-alias", default="candidate")
    paper_deploy.add_argument("--symbols", default="BTCUSDT,ETHUSDT")
    paper_deploy.add_argument("--json", action="store_true")
    portfolio_ops = sub.add_parser("paper-portfolio-ops")
    portfolio_ops.add_argument("--quote-budget", default="1000")
    portfolio_ops.add_argument("--json", action="store_true")
    portfolio_benchmark = sub.add_parser("paper-portfolio-benchmark")
    portfolio_benchmark.add_argument("--quote-budget", default="1000")
    portfolio_benchmark.add_argument("--json", action="store_true")
    portfolio_optimize = sub.add_parser("paper-portfolio-optimize")
    portfolio_optimize.add_argument("--quote-budget", default="1000")
    portfolio_optimize.add_argument("--json", action="store_true")
    policy_rollout = sub.add_parser("paper-policy-rollout")
    policy_rollout.add_argument("--symbols", default="BTCUSDT,ETHUSDT,BNBUSDT")
    policy_rollout.add_argument("--json", action="store_true")
    policy_register = sub.add_parser("policy-register")
    policy_register.add_argument("--policy-id", default="demo-policy")
    policy_register.add_argument("--json", action="store_true")
    policy_promote = sub.add_parser("policy-promote")
    policy_promote.add_argument("--policy-id", required=True)
    policy_promote.add_argument("--confirm", default="")
    policy_promote.add_argument("--json", action="store_true")
    rollout_plan_cmd = sub.add_parser("policy-rollout-plan")
    rollout_plan_cmd.add_argument("--champion", default="champion")
    rollout_plan_cmd.add_argument("--challenger", default="challenger")
    rollout_plan_cmd.add_argument("--stage", default="10pct")
    rollout_plan_cmd.add_argument("--json", action="store_true")
    ab_start = sub.add_parser("ab-paper-start")
    ab_start.add_argument("--rollout-id", default="")
    ab_start.add_argument("--confirm", default="")
    ab_start.add_argument("--json", action="store_true")
    ab_status = sub.add_parser("ab-paper-status")
    ab_status.add_argument("--experiment-id", default="")
    ab_status.add_argument("--json", action="store_true")
    ab_stop = sub.add_parser("ab-paper-stop")
    ab_stop.add_argument("--experiment-id", default="")
    ab_stop.add_argument("--reason", default="operator_stop")
    ab_stop.add_argument("--json", action="store_true")
    governance_cmd = sub.add_parser("governance-decision")
    governance_cmd.add_argument("--experiment-id", default="")
    governance_cmd.add_argument("--json", action="store_true")
    weekly_governance = sub.add_parser("weekly-governance-report")
    weekly_governance.add_argument("--json", action="store_true")
    policy_rollback = sub.add_parser("policy-rollback")
    policy_rollback.add_argument("--to", default="previous-champion")
    policy_rollback.add_argument("--confirm", default="")
    policy_rollback.add_argument("--json", action="store_true")
    governance_bundle = sub.add_parser("governance-evidence-bundle")
    governance_bundle.add_argument("--json", action="store_true")
    governance_sim = sub.add_parser("governance-simulation")
    governance_sim.add_argument("--case", default="challenger_beats")
    governance_sim.add_argument("--json", action="store_true")
    local_ops_jobs = sub.add_parser("local-ops-jobs")
    local_ops_jobs.add_argument("--json", action="store_true")
    metrics_report = sub.add_parser("metrics-warehouse-report")
    metrics_report.add_argument("--json", action="store_true")
    ops_assistant = sub.add_parser("ops-assistant-query")
    ops_assistant.add_argument("--question", required=True)
    ops_assistant.add_argument("--json", action="store_true")
    action_center = sub.add_parser("action-center-propose")
    action_center.add_argument("--type", default="export_report")
    action_center.add_argument("--reason", default="operator requested safe local action")
    action_center.add_argument("--approve", action="store_true")
    action_center.add_argument("--json", action="store_true")
    permission_report = sub.add_parser("permission-report")
    permission_report.add_argument("--json", action="store_true")
    permission_check = sub.add_parser("permission-check")
    permission_check.add_argument("--role", default="operator")
    permission_check.add_argument("--action", default="start_demo")
    permission_check.add_argument("--json", action="store_true")
    dr_drill = sub.add_parser("disaster-recovery-drill")
    dr_drill.add_argument("--bundle", default="")
    dr_drill.add_argument("--json", action="store_true")
    sub.add_parser("security-scan")
    backtest = sub.add_parser("demo-backtest")
    backtest.add_argument("--raw-klines-json", required=False)
    run_local = sub.add_parser("run-local")
    run_local.add_argument("--mode", choices=["demo", "paper", "testnet-readiness"], default="demo")
    run_local.add_argument("--symbol", default="BTCUSDT")
    run_local.add_argument("--interval", default="1m")
    run_local.add_argument("--scenario", default="sideways")
    run_local.add_argument("--source", choices=["auto", "demo", "rest", "websocket"], default="auto")
    run_local.add_argument("--model-alias", default="")
    run_local.add_argument("--steps", type=int, default=100)
    run_local.add_argument("--demo-trading-armed", action="store_true")
    run_local.add_argument("--demo-pilot-preset", choices=["smoke", "operator", "endurance"], default="smoke")
    stream_paper = sub.add_parser("stream-paper")
    stream_paper.add_argument("--symbol", default="BTCUSDT")
    stream_paper.add_argument("--interval", default="1m")
    stream_paper.add_argument("--source", choices=["demo", "rest", "websocket"], default="websocket")
    stream_paper.add_argument("--steps", type=int, default=120)
    paper_session = sub.add_parser("paper-session")
    paper_session.add_argument("--symbol", default="BTCUSDT")
    paper_session.add_argument("--interval", default="1m")
    paper_session.add_argument("--minutes", type=int, default=15)
    paper_session.add_argument("--max-steps", type=int, default=200)
    paper_session.add_argument("--max-paper-orders", type=int, default=25)
    paper_session.add_argument("--max-critical-alerts", type=int, default=1)
    paper_session.add_argument("--source", choices=["auto", "demo", "rest", "websocket"], default="demo")
    sub.add_parser("list-sessions")
    show_session = sub.add_parser("show-session")
    show_session.add_argument("--session-id", required=True)
    export_report = sub.add_parser("export-session-report")
    export_report.add_argument("--session-id", required=True)
    sub.add_parser("pilot-status")
    pilot_preflight = sub.add_parser("pilot-preflight")
    pilot_preflight.add_argument("--symbol", default="BTCUSDT")
    pilot_preflight.add_argument("--interval", default="1m")
    pilot_preflight.add_argument("--preset", choices=["smoke", "operator", "endurance"], default="smoke")
    pilot_report = sub.add_parser("pilot-report")
    pilot_report.add_argument("--run-id", default="")
    runner_start = sub.add_parser("pilot-runner-start")
    runner_start.add_argument("--symbol", default="BTCUSDT")
    runner_start.add_argument("--interval", default="1m")
    runner_start.add_argument("--preset", choices=["smoke", "operator", "endurance"], default="smoke")
    runner_start.add_argument("--source", choices=["demo", "rest", "websocket", "auto"], default="demo")
    runner_start.add_argument("--max-steps", type=int, default=0)
    runner_start.add_argument("--foreground", action="store_true")
    sub.add_parser("pilot-runner-status")
    sub.add_parser("pilot-runner-stop")
    runner_command = sub.add_parser("pilot-runner-command")
    runner_command.add_argument("--type", choices=["stop", "reconcile", "cancel_open_orders", "export_report"], required=True)
    register_model = sub.add_parser("register-demo-model")
    register_model.add_argument("--alias", default="candidate")
    promote_model = sub.add_parser("promote-model")
    promote_model.add_argument("--model-id", required=True)
    promote_model.add_argument("--confirm", action="store_true")
    evaluate = sub.add_parser("evaluate-model")
    evaluate.add_argument("--symbol", default="BTCUSDT")
    evaluate.add_argument("--interval", default="1m")
    evaluate.add_argument("--scenario", default="sideways")
    evaluate.add_argument("--walk-forward", action="store_true")
    quality = sub.add_parser("data-quality")
    quality.add_argument("--symbol", default="BTCUSDT")
    quality.add_argument("--interval", default="1m")
    quality.add_argument("--scenario", default="sideways")
    connectivity = sub.add_parser("connectivity-check")
    connectivity.add_argument("--symbol", default="BTCUSDT")
    launch = sub.add_parser("launch-dashboard")
    launch.add_argument("--start-port", type=int, default=8503)
    control_center = sub.add_parser("control-center")
    control_center.add_argument("--start-port", type=int, default=8503)
    control_center.add_argument("--no-browser", action="store_true")
    control_center.add_argument("--dry-run", action="store_true")
    check_all = sub.add_parser("check-all")
    check_all.add_argument("--json", action="store_true")
    check_all.add_argument("--skip-tests", action="store_true")
    evidence_scorecard = sub.add_parser("evidence-scorecard")
    evidence_scorecard.add_argument("--json", action="store_true")
    evidence_scorecard.add_argument("--strict", action="store_true")
    rehearsal = sub.add_parser("demo-acceptance-rehearsal")
    rehearsal.add_argument("--browser-url", default="")
    rehearsal.add_argument("--json", action="store_true")
    rehearsal.add_argument("--strict", action="store_true")
    dashboard_smoke = sub.add_parser("dashboard-smoke")
    dashboard_smoke.add_argument("--seconds", type=int, default=10)
    browser_smoke = sub.add_parser("dashboard-browser-smoke")
    browser_smoke.add_argument("--url", required=True)
    browser_smoke.add_argument("--seconds", type=int, default=15)
    browser_smoke.add_argument("--update-baseline", action="store_true")
    operator_evidence = sub.add_parser("dashboard-operator-evidence")
    operator_evidence.add_argument("--mode", default="demo")
    operator_evidence.add_argument("--profile", default="local-demo")
    operator_evidence.add_argument("--source", default="demo")
    demo_preview = sub.add_parser("demo-execution-preview")
    demo_preview.add_argument("--symbol", default="BTCUSDT")
    demo_preview.add_argument("--side", choices=["BUY", "SELL"], default="BUY")
    demo_preview.add_argument("--quote-size", default="10")
    demo_preview.add_argument("--last-price", default="100")
    demo_test = sub.add_parser("demo-execution-test-order")
    demo_test.add_argument("--symbol", default="BTCUSDT")
    demo_test.add_argument("--side", choices=["BUY", "SELL"], default="BUY")
    demo_test.add_argument("--quote-size", default="10")
    demo_test.add_argument("--last-price", default="100")
    demo_place = sub.add_parser("demo-execution-place")
    demo_place.add_argument("--symbol", default="BTCUSDT")
    demo_place.add_argument("--side", choices=["BUY", "SELL"], default="BUY")
    demo_place.add_argument("--quote-size", default="10")
    demo_place.add_argument("--last-price", default="100")
    demo_place.add_argument("--armed", action="store_true")
    demo_place.add_argument("--confirm-demo-order", action="store_true")
    demo_query = sub.add_parser("demo-execution-query")
    demo_query.add_argument("--symbol", default="BTCUSDT")
    demo_query.add_argument("--order-id", type=int, default=0)
    demo_query.add_argument("--client-order-id", default="")
    demo_cancel = sub.add_parser("demo-execution-cancel")
    demo_cancel.add_argument("--symbol", default="BTCUSDT")
    demo_cancel.add_argument("--order-id", type=int, required=True)
    demo_cancel.add_argument("--confirm-cancel", action="store_true")
    sub.add_parser("demo-execution-report")
    dashboard = sub.add_parser("dashboard")
    dashboard.add_argument("--mode", choices=["demo", "paper", "testnet-readiness"], default="demo")
    dashboard.add_argument("--symbol", default="BTCUSDT")
    dashboard.add_argument("--interval", default="1m")
    dashboard.add_argument("--source", choices=["auto", "demo", "rest", "websocket"], default="auto")
    args = parser.parse_args()
    settings = BotSettings.from_env()
    if args.command == "validate-config":
        settings.validate_startup()
        print(json.dumps({"status": "ok", "mode": settings.trading_mode.value}))
        return
    if args.command == "preflight":
        report = run_preflight(settings, Path.cwd())
        print(json.dumps(report.to_dict(), default=str))
        if report.status != "ok":
            raise SystemExit(1)
        return
    if args.command == "diagnostics":
        payload = collect_diagnostics(settings).to_dict()
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        if args.strict and payload.get("status") != "ok":
            raise SystemExit(1)
        return
    if args.command == "support-bundle":
        output = Path(args.output) if args.output else settings.data_dir / "support" / "support-bundle.zip"
        print(json.dumps(create_support_bundle(settings, output), indent=2 if args.json else None, default=str))
        return
    if args.command == "support-bundle-verify":
        print(json.dumps(verify_support_bundle(Path(args.bundle)), indent=2 if args.json else None, default=str))
        return
    if args.command == "retention-preview":
        print(json.dumps(retention_preview(settings, older_than_days=args.older_than_days), indent=2 if args.json else None, default=str))
        return
    if args.command == "state-archive":
        output = Path(args.output) if args.output else settings.data_dir / "support" / "state-archive.zip"
        print(json.dumps(create_state_archive(settings, output, older_than_days=args.older_than_days), indent=2 if args.json else None, default=str))
        return
    if args.command == "incident-timeline":
        payload = {"markdown": str(write_timeline_markdown(settings))} if args.markdown else {"events": incident_timeline(settings), "live_trading_enabled": False}
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "operator-report":
        print(json.dumps(export_operator_report(settings), indent=2 if args.json else None, default=str))
        return
    if args.command == "operator-quality-gate":
        payload = operator_quality_gate(settings)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        if args.strict and payload.get("status") != "ok":
            raise SystemExit(1)
        return
    if args.command == "artifact-catalog":
        print(
            json.dumps(
                artifact_catalog(settings, category=args.category, suffix=args.suffix, stale_days=args.stale_days),
                indent=2 if args.json else None,
                default=str,
            )
        )
        return
    if args.command == "operator-health-score":
        print(json.dumps(operator_health_score(settings), indent=2 if args.json else None, default=str))
        return
    if args.command == "rehearsal-profiles":
        print(json.dumps(rehearsal_profiles(), indent=2 if args.json else None, default=str))
        return
    if args.command == "operator-report-diff":
        print(json.dumps(operator_report_diff(settings), indent=2 if args.json else None, default=str))
        return
    if args.command == "support-bundle-restore-preview":
        print(
            json.dumps(
                support_bundle_restore_preview(Path(args.bundle)),
                indent=2 if args.json else None,
                default=str,
            )
        )
        return
    if args.command == "evidence-chain":
        print(json.dumps(evidence_chain(settings), indent=2 if args.json else None, default=str))
        return
    if args.command == "environment-doctor":
        print(json.dumps(environment_doctor(settings), indent=2 if args.json else None, default=str))
        return
    if args.command == "data-growth-budget":
        print(
            json.dumps(
                data_growth_budget(settings, budget_bytes=args.budget_bytes),
                indent=2 if args.json else None,
                default=str,
            )
        )
        return
    if args.command == "diagnostics-baseline":
        print(json.dumps(diagnostics_baseline(settings, write=args.write), indent=2 if args.json else None, default=str))
        return
    if args.command == "report-index":
        print(json.dumps(report_index(settings), indent=2 if args.json else None, default=str))
        return
    if args.command == "support-bundles-verify":
        print(json.dumps(verify_support_bundles(settings), indent=2 if args.json else None, default=str))
        return
    if args.command == "redaction-self-test":
        payload = redaction_self_test()
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        if payload.get("status") != "ok":
            raise SystemExit(1)
        return
    if args.command == "local-ops-snapshot":
        print(json.dumps(local_ops_snapshot(settings), indent=2 if args.json else None, default=str))
        return
    if args.command == "operator-command-manifest":
        print(json.dumps(operator_command_manifest(), indent=2 if args.json else None, default=str))
        return
    if args.command == "evidence-manifest":
        print(json.dumps(write_evidence_manifest(settings), indent=2 if args.json else None, default=str))
        return
    if args.command == "fetch-public-data":
        service = BinanceDataIngestionService(settings)
        result = service.ingest(
            IngestionRequest(
                symbols=_csv_arg(args.symbols),
                intervals=_csv_arg(args.intervals),
                candle_limit=args.limit,
            )
        )
        export_public_data_evidence(settings, result)
        print(json.dumps(result.to_dict(), indent=2 if args.json else None, default=str))
        if result.status != "ok":
            raise SystemExit(1)
        return
    if args.command == "warmup-indicators":
        payload = warmup_indicators(settings, _csv_arg(args.symbols), candle_limit=args.limit)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        if payload.get("status") == "blocked":
            raise SystemExit(1)
        return
    if args.command == "public-data-status":
        print(json.dumps(BinanceDataIngestionService(settings).cache_status(), default=str))
        return
    if args.command == "clear-public-data-cache":
        print(json.dumps(BinanceDataIngestionService(settings).clear_cache(args.confirm), default=str))
        return
    if args.command == "public-data-evidence":
        path = export_public_data_evidence(settings)
        payload = {"status": "ok", "path": str(path), "live_trading_enabled": False}
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "strategy-calibrate":
        candles_by_symbol = {
            symbol: _load_or_demo_candles(settings, symbol, args.interval, args.scenario)
            for symbol in _csv_arg(args.symbols)
        }
        result = calibrate_strategy(settings.data_dir, candles_by_symbol, interval=args.interval)
        print(json.dumps(result.to_dict(), indent=2 if args.json else None, default=str))
        if result.status != "ready":
            raise SystemExit(1)
        return
    if args.command == "paper-deployment-cycle":
        observations = [
            {"symbol": symbol, "pnl": "1.0", "confidence": 0.58}
            for symbol in _csv_arg(args.symbols)
        ]
        payload = run_paper_deployment_cycle(
            settings,
            args.strategy_id,
            args.model_alias,
            _csv_arg(args.symbols),
            observations,
            calibration_gate={"status": "paper_approved"},
        )
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "paper-portfolio-ops":
        payload = run_portfolio_operations(
            settings,
            [
                PaperStrategy("adaptive", 0.72, ["BTCUSDT", "ETHUSDT"]),
                PaperStrategy("mean-reversion", 0.61, ["ETHUSDT", "BNBUSDT"]),
            ],
            Decimal(str(args.quote_budget)),
            [{"strategy_id": "adaptive", "pnl": "2.5"}, {"strategy_id": "mean-reversion", "pnl": "-1.0"}],
        )
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "paper-portfolio-benchmark":
        ops = run_portfolio_operations(
            settings,
            [
                PaperStrategy("adaptive", 0.72, ["BTCUSDT", "ETHUSDT"]),
                PaperStrategy("mean-reversion", 0.61, ["BNBUSDT"]),
            ],
            Decimal(str(args.quote_budget)),
            [],
        )
        from .paper_portfolio_ops import PaperPortfolioPlan

        plan = PaperPortfolioPlan(
            portfolio_id=ops["plan"]["portfolio_id"],
            total_quote_budget=Decimal(str(ops["plan"]["total_quote_budget"])),
            allocations=ops["plan"]["allocations"],
            conflicts=ops["plan"]["conflicts"],
            risk_limits=ops["plan"]["risk_limits"],
            rotation=ops["plan"]["rotation"],
        )
        benchmark = benchmark_allocations(plan)
        benchmark["reports"] = write_benchmark_report(settings, benchmark)
        print(json.dumps(benchmark, indent=2 if args.json else None, default=str))
        return
    if args.command == "paper-portfolio-optimize":
        ops = run_portfolio_operations(
            settings,
            [
                PaperStrategy("adaptive", 0.72, ["BTCUSDT", "ETHUSDT"]),
                PaperStrategy("mean-reversion", 0.61, ["BNBUSDT"]),
            ],
            Decimal(str(args.quote_budget)),
            [],
        )
        from .paper_portfolio_ops import PaperPortfolioPlan

        plan = PaperPortfolioPlan(
            portfolio_id=ops["plan"]["portfolio_id"],
            total_quote_budget=Decimal(str(ops["plan"]["total_quote_budget"])),
            allocations=ops["plan"]["allocations"],
            conflicts=ops["plan"]["conflicts"],
            risk_limits=ops["plan"]["risk_limits"],
            rotation=ops["plan"]["rotation"],
        )
        payload = optimize_portfolio_policy(settings, plan)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "paper-policy-rollout":
        payload = run_policy_rollout(settings, _csv_arg(args.symbols))
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "policy-register":
        registry = PortfolioPolicyRegistry(settings.data_dir / "portfolio-policies")
        policy = registry.register(demo_policy(args.policy_id))
        print(json.dumps(policy.to_dict(), indent=2 if args.json else None, default=str))
        return
    if args.command == "policy-promote":
        registry = PortfolioPolicyRegistry(settings.data_dir / "portfolio-policies")
        try:
            policy = registry.get(args.policy_id)
        except KeyError:
            policy = registry.register(demo_policy(args.policy_id))
        gate = evaluate_policy_promotion(policy, operator_confirmed=args.confirm == "PAPER_POLICY_PROMOTE")
        if gate.allowed:
            decision = registry.set_champion(args.policy_id, operator_confirmed=True)
            payload = {"gate": gate.__dict__, "decision": decision.__dict__, "live_trading_enabled": False}
        else:
            payload = {"gate": gate.__dict__, "decision": "blocked", "live_trading_enabled": False}
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        if not gate.allowed:
            raise SystemExit(1)
        return
    if args.command == "policy-rollout-plan":
        plan = create_rollout_plan(
            args.champion,
            args.challenger,
            ["BTCUSDT", "ETHUSDT"],
            stage=args.stage,
            challenger_pct=10,
            operator_confirmation="PAPER_POLICY_ROLLOUT" if args.stage in {"25pct", "50pct", "full_paper"} else "",
        )
        print(json.dumps(plan.to_dict(), indent=2 if args.json else None, default=str))
        return
    if args.command == "ab-paper-start":
        if args.confirm != "PAPER_AB":
            print(json.dumps({"status": "blocked", "reason": "PAPER_AB confirmation required", "live_trading_enabled": False}))
            raise SystemExit(1)
        plan = create_rollout_plan("champion", "challenger", ["BTCUSDT", "ETHUSDT"], challenger_pct=50)
        report = run_ab_paper_experiment(
            plan,
            [
                {"symbol": "BTCUSDT", "variant": "champion", "pnl": "1", "drawdown": "1"},
                {"symbol": "ETHUSDT", "variant": "challenger", "pnl": "2", "drawdown": "1"},
            ],
        )
        path = write_ab_experiment_report(settings.data_dir, report)
        print(json.dumps({"path": str(path), **report}, indent=2 if args.json else None, default=str))
        return
    if args.command == "ab-paper-status":
        path = settings.data_dir / "policy-governance" / "ab-experiments"
        latest = sorted(path.glob("*.json"))[-1] if path.exists() and list(path.glob("*.json")) else None
        payload = json.loads(latest.read_text(encoding="utf-8")) if latest else {"status": "missing", "live_trading_enabled": False}
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "ab-paper-stop":
        payload = {"status": "stopped", "experiment_id": args.experiment_id, "reason": args.reason, "live_trading_enabled": False}
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "governance-decision":
        experiment = run_governance_simulation("challenger_beats")["experiment"]
        stop = evaluate_stopping_rules(experiment, min_samples=1)
        payload = governance_decision(experiment, stop, operator_confirmed=False)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "weekly-governance-report":
        payload = run_governance_simulation("challenger_beats")
        paths = write_weekly_governance_report(settings.data_dir, {"current_champion": "champion", "decision": payload["decision"]})
        print(json.dumps({"paths": paths, **payload}, indent=2 if args.json else None, default=str))
        return
    if args.command == "policy-rollback":
        registry = PortfolioPolicyRegistry(settings.data_dir / "portfolio-policies")
        for policy_id in ("previous", "current"):
            try:
                registry.get(policy_id)
            except KeyError:
                registry.register(demo_policy(policy_id))
        champion = registry.champion()
        if not champion or not champion.previous_champion_id:
            registry.set_champion("previous", operator_confirmed=True)
            registry.set_champion("current", operator_confirmed=True)
        payload = rollback_to_previous_champion(registry, confirm=args.confirm)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        if payload.get("status") != "rolled_back":
            raise SystemExit(1)
        return
    if args.command == "governance-evidence-bundle":
        report = run_governance_simulation("challenger_beats")
        marker = settings.data_dir / "policy-governance" / "bundle-source.json"
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
        payload = export_governance_evidence_bundle(settings.data_dir, [marker], {"source": "cli"})
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "governance-simulation":
        payload = run_governance_simulation(args.case)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "local-ops-jobs":
        payload = generate_scheduled_ops_report(settings)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "metrics-warehouse-report":
        payload = write_metrics_report(
            settings,
            [{"equity": 1000, "pnl_quote": 1.25, "latency_ms": 42}, {"equity": 1001.25, "pnl_quote": 0.25, "latency_ms": 38}],
        )
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        return
    if args.command == "ops-assistant-query":
        payload = write_ops_assistant_answer(settings, args.question)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        if payload.get("status") == "blocked":
            raise SystemExit(1)
        return
    if args.command == "action-center-propose":
        payload = create_reviewed_action(settings, args.type, args.reason, approved=args.approve)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        if payload.get("review", {}).get("status", "").startswith("blocked"):
            raise SystemExit(1)
        return
    if args.command == "permission-report":
        payload = permission_compliance_report(settings)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        if payload.get("status") != "ok":
            raise SystemExit(1)
        return
    if args.command == "permission-check":
        payload = evaluate_permission(args.role, args.action)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        if not payload.get("allowed"):
            raise SystemExit(1)
        return
    if args.command == "disaster-recovery-drill":
        payload = run_disaster_recovery_drill(settings, bundle_zip=Path(args.bundle) if args.bundle else None)
        print(json.dumps(payload, indent=2 if args.json else None, default=str))
        if payload.get("status") not in {"pass", "warn"}:
            raise SystemExit(1)
        return
    if args.command == "security-scan":
        findings = scan_for_secrets(settings.data_dir.parent if settings.data_dir.parent else settings.data_dir)
        print(json.dumps({"findings": [[str(p), line, msg] for p, line, msg in findings]}))
        if findings:
            raise SystemExit(1)
        return
    if args.command == "demo-backtest":
        datastore = DataStore(settings.data_dir)
        raw = json.loads(open(args.raw_klines_json, encoding="utf-8").read()) if args.raw_klines_json else _demo_klines()
        candles = parse_binance_klines(raw)
        features = build_feature_rows("BTCUSDT", candles, window=5)
        labels = build_label_rows(candles, window=5, horizon_bars=2)
        model = TinyNeuralSignalModel()
        model.fit(features, labels, epochs=5)
        limits = _default_limits()
        audit = AuditLog(settings.audit_log_path)
        audit.emit("cli", "demo_backtest_started", {})
        result = BacktestEngine(RiskEngine(limits, kill_switch=False)).run(features, model)
        datastore.save_feature_rows("demo", features)
        datastore.save_label_rows("demo", labels)
        print(json.dumps(result.__dict__, default=str))
        return
    if args.command in {"run-local", "stream-paper"}:
        mode = "paper" if args.command == "stream-paper" else args.mode
        runtime = BotRuntime(
            settings,
            RuntimeOptions(
                mode=mode,
                symbol=args.symbol,
                interval=args.interval,
                scenario=getattr(args, "scenario", "sideways"),
                source=args.source,
                model_alias=getattr(args, "model_alias", ""),
                demo_trading_armed=getattr(args, "demo_trading_armed", False),
                demo_pilot_preset=getattr(args, "demo_pilot_preset", "smoke"),
            ),
        )
        snapshot = runtime.run_steps(args.steps)
        print(json.dumps(_runtime_summary(snapshot_to_dict(snapshot)), default=str))
        return
    if args.command == "paper-session":
        runtime = BotRuntime(
            settings,
            RuntimeOptions(
                mode="paper",
                symbol=args.symbol,
                interval=args.interval,
                source=args.source,
                fetch_limit=max(args.max_steps, 80),
            ),
        )
        started = time.time()
        snapshot = runtime.snapshot()
        try:
            for step in range(max(1, args.max_steps)):
                if time.time() - started > max(1, args.minutes) * 60:
                    runtime.message = "paper session time budget reached"
                    break
                snapshot = runtime.step()
                runtime.session_store.record_heartbeat(
                    runtime.session.session_id,
                    {"step": step + 1, "status": snapshot.status, "equity": str(snapshot.equity)},
                )
                critical = len([alert for alert in snapshot.alerts if alert.get("severity") == "critical"])
                if len(snapshot.fills) >= args.max_paper_orders or critical >= args.max_critical_alerts:
                    runtime.stop()
                    snapshot = runtime.snapshot()
                    break
                if snapshot.status in {"completed", "stopped"}:
                    break
        except KeyboardInterrupt:
            runtime.stop()
            snapshot = runtime.snapshot()
        finally:
            if snapshot.status not in {"completed", "stopped"}:
                runtime.stop()
                snapshot = runtime.snapshot()
        print(
            json.dumps(
                {
                    **_runtime_summary(snapshot_to_dict(snapshot)),
                    "report_paths": snapshot.report_paths,
                    "alerts": len(snapshot.alerts),
                    "paper_account": snapshot.paper_account,
                },
                default=str,
            )
        )
        return
    if args.command == "list-sessions":
        sessions = SessionStore(settings.data_dir / "sessions").list_sessions(5)
        print(json.dumps([session.__dict__ for session in sessions], default=str))
        return
    if args.command == "show-session":
        store = SessionStore(settings.data_dir / "sessions")
        summary = store.load_summary(args.session_id)
        fills_csv = store.export_fills_csv(args.session_id)
        print(
            json.dumps(
                {
                    "summary": summary.__dict__,
                    "snapshot_export": str(store.export_session_jsonl(args.session_id)),
                    "fills_export": str(fills_csv),
                    "snapshots": store.load_events(args.session_id)[-5:],
                },
                default=str,
            )
        )
        return
    if args.command == "export-session-report":
        store = SessionStore(settings.data_dir / "sessions")
        print(json.dumps(export_session_report(store, args.session_id), default=str))
        return
    if args.command == "pilot-status":
        store = PilotRunStore(settings.data_dir / "pilot-runs")
        latest = store.latest()
        unfinished = store.latest_non_terminal()
        print(
            json.dumps(
                {
                    "latest": latest.to_dict() if latest else {},
                    "unfinished": unfinished.to_dict() if unfinished else {},
                    "live_trading_enabled": False,
                },
                default=str,
            )
        )
        return
    if args.command == "pilot-preflight":
        runtime = BotRuntime(
            settings,
            RuntimeOptions(
                mode="demo",
                symbol=args.symbol,
                interval=args.interval,
                source="demo",
                demo_trading_armed=False,
                demo_pilot_preset=args.preset,
            ),
        )
        snapshot = snapshot_to_dict(runtime.snapshot())
        orchestrator = DemoPilotOrchestrator(settings, PilotRunStore(settings.data_dir / "pilot-runs"))
        print(json.dumps(orchestrator.evaluate_start_gate(snapshot), default=str))
        return
    if args.command == "pilot-report":
        store = PilotRunStore(settings.data_dir / "pilot-runs")
        run = store.load(args.run_id) if args.run_id else store.latest()
        print(json.dumps(run.to_dict() if run else {}, default=str))
        return
    if args.command == "pilot-runner-start":
        if args.foreground:
            service = PilotRunnerService(settings)
            print(
                json.dumps(
                    service.run(
                        symbol=args.symbol,
                        interval=args.interval,
                        preset=args.preset,
                        source=args.source,
                        max_steps=args.max_steps,
                        sleep_seconds=1.0,
                    ),
                    default=str,
                )
            )
        else:
            print(
                json.dumps(
                    start_background_runner(
                        symbol=args.symbol,
                        interval=args.interval,
                        preset=args.preset,
                        source=args.source,
                        cwd=Path.cwd(),
                    ),
                    default=str,
                )
            )
        return
    if args.command == "pilot-runner-status":
        print(json.dumps(PilotRunnerService(settings).status(), default=str))
        return
    if args.command == "pilot-runner-stop":
        service = PilotRunnerService(settings)
        print(json.dumps(service.enqueue_command("stop"), default=str))
        return
    if args.command == "pilot-runner-command":
        service = PilotRunnerService(settings)
        print(json.dumps(service.enqueue_command(args.type), default=str))
        return
    if args.command == "register-demo-model":
        datastore = DataStore(settings.data_dir)
        candles = DemoMarketReplay(count=160).candles()
        features = build_feature_rows("BTCUSDT", candles, window=5)
        labels = build_label_rows(candles, window=5, horizon_bars=2)
        evaluation_report = evaluate_walk_forward("BTCUSDT", "1m", candles)
        eval_path = settings.data_dir / "evaluations" / "BTCUSDT_1m_walkforward_latest.json"
        eval_path.parent.mkdir(parents=True, exist_ok=True)
        eval_payload = report_to_dict(evaluation_report)
        eval_path.write_text(json.dumps(eval_payload, indent=2, default=str), encoding="utf-8")
        manifest_path = settings.data_dir / "datasets" / "demo-replay-manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(eval_payload["manifest"], indent=2, default=str), encoding="utf-8")
        ExperimentDB(settings.data_dir / "experiments" / "experiments.json").add_walkforward_eval(
            str(eval_path),
            {
                "dataset_id": "demo-replay",
                "status": "completed",
                "candidate_beats_baseline": eval_payload["candidate_summary"]["beats_baseline"],
            },
        )
        model = TinyNeuralSignalModel()
        model.fit(features, labels, epochs=10)
        registry = ModelRegistry(datastore.models_dir)
        metadata = registry.register(
            model,
            alias=args.alias,
            dataset_id="demo-replay",
            feature_schema_hash=eval_payload["manifest"]["feature_schema_hash"],
            manifest_path=str(manifest_path),
            walkforward_report_path=str(eval_path),
            train_range=f"{features[0].timestamp_ms}-{features[len(features)//2].timestamp_ms}",
            validation_range="chronological-demo-validation",
            test_range=f"{features[-40].timestamp_ms}-{features[-1].timestamp_ms}",
            metrics={
                "train_rows": len(features),
                "label_rows": len(labels),
                "epochs": 10,
                "leakage_pass": eval_payload["leakage"]["passed"],
                "candidate_beats_baseline": eval_payload["candidate_summary"]["beats_baseline"],
                "trade_count": sum(fold["candidate"]["trades"] for fold in eval_payload["folds"]),
                "min_trade_count": 1,
                "max_drawdown_quote": max(float(fold["candidate"]["max_drawdown"]) for fold in eval_payload["folds"]),
                "max_allowed_drawdown_quote": 100,
            },
        )
        ExperimentDB(settings.data_dir / "experiments" / "experiments.json").add_model_card(
            metadata.model_card_path,
            {"dataset_id": metadata.dataset_id, "model_id": metadata.model_id, "status": metadata.status},
        )
        print(json.dumps(metadata.__dict__, default=str))
        return
    if args.command == "promote-model":
        registry = ModelRegistry(settings.data_dir / "models")
        decision = registry.promote_to_champion(args.model_id, operator_confirmed=args.confirm)
        decision_path = settings.data_dir / "models" / f"{args.model_id}-promotion-decision.json"
        decision_path.write_text(json.dumps(decision.to_dict(), indent=2), encoding="utf-8")
        ExperimentDB(settings.data_dir / "experiments" / "experiments.json").add_promotion_decision(
            str(decision_path),
            {"model_id": args.model_id, "status": "allowed" if decision.allowed else "blocked"},
        )
        print(json.dumps(decision.to_dict(), default=str))
        if not decision.allowed:
            raise SystemExit(1)
        return
    if args.command == "evaluate-model":
        candles = _load_or_demo_candles(settings, args.symbol, args.interval, args.scenario)
        if args.walk_forward:
            report = evaluate_walk_forward(
                args.symbol,
                args.interval,
                candles,
                dataset_id=f"{args.symbol}_{args.interval}_walkforward",
                config=WalkForwardConfig(),
            )
            suffix = "walkforward_latest"
        else:
            report = evaluate_rule_baseline(args.symbol, args.interval, candles)
            suffix = "latest"
        path = settings.data_dir / "evaluations" / f"{args.symbol}_{args.interval}_{suffix}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report_to_dict(report), indent=2, default=str), encoding="utf-8")
        payload = report_to_dict(report)
        if payload.get("manifest"):
            manifest_path = settings.data_dir / "datasets" / f"{payload['manifest']['dataset_id']}.json"
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(json.dumps(payload["manifest"], indent=2, default=str), encoding="utf-8")
            ExperimentDB(settings.data_dir / "experiments" / "experiments.json").add_dataset_manifest(
                str(manifest_path),
                {"dataset_id": payload["manifest"]["dataset_id"], "status": payload["leakage"]["status"]},
            )
        manifest_payload = payload.get("manifest") or {}
        ExperimentDB(settings.data_dir / "experiments" / "experiments.json").add(
            "walkforward_eval" if args.walk_forward else "evaluation",
            str(path),
            {"dataset_id": manifest_payload.get("dataset_id", ""), "status": "completed"},
        )
        print(json.dumps({"path": str(path), **report_to_dict(report)}, default=str))
        return
    if args.command == "data-quality":
        candles = _load_or_demo_candles(settings, args.symbol, args.interval, args.scenario)
        report = check_candles(candles, now_ms=candles[-1].close_time_ms if candles else None)
        print(json.dumps(report.to_dict(), default=str))
        return
    if args.command == "connectivity-check":
        print(json.dumps(connectivity_report(settings, args.symbol), default=str))
        return
    if args.command == "launch-dashboard":
        port = find_free_port(args.start_port)
        print(json.dumps({"port": port, "url": f"http://127.0.0.1:{port}", "live_trading_enabled": False}))
        return
    if args.command == "control-center":
        result = start_control_center(
            Path.cwd(),
            start_port=args.start_port,
            open_browser=not args.no_browser,
            dry_run=args.dry_run,
        )
        print(json.dumps(result.to_dict(), default=str))
        return
    if args.command == "check-all":
        payload = payload_for(run_checks(Path.cwd(), skip_tests=args.skip_tests))
        print_payload(payload, as_json=args.json)
        if payload["status"] != "ok":
            raise SystemExit(1)
        return
    if args.command == "evidence-scorecard":
        from .evidence_scorecard import generate_evidence_scorecard, write_scorecard

        scorecard = generate_evidence_scorecard(settings, write=False)
        path = write_scorecard(settings, scorecard)
        payload = {"path": str(path), **scorecard.to_dict()}
        print(json.dumps(payload, default=str) if args.json else json.dumps(payload, indent=2, default=str))
        if args.strict and scorecard.status != "pass":
            raise SystemExit(1)
        return
    if args.command == "demo-acceptance-rehearsal":
        from .demo_acceptance_rehearsal import DemoAcceptanceRehearsal

        summary = DemoAcceptanceRehearsal(settings, Path.cwd()).run(browser_url=args.browser_url)
        payload = summary.to_dict()
        print(json.dumps(payload, default=str) if args.json else json.dumps(payload, indent=2, default=str))
        if args.strict and summary.status != "pass":
            raise SystemExit(1)
        return
    if args.command == "dashboard-smoke":
        from .ui.chart_registry import all_chart_keys
        from .ui.page_registry import PAGES, validate_page_registry

        validate_page_registry()
        chart_keys = all_chart_keys()
        payload = {
            "status": "ok",
            "seconds": args.seconds,
            "pages": [page.key for page in PAGES],
            "chart_keys": list(chart_keys),
            "unique_chart_keys": len(chart_keys) == len(set(chart_keys)),
            "live_trading_enabled": False,
        }
        out = settings.data_dir / "checks" / "dashboard-smoke.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(json.dumps({"path": str(out), **payload}))
        return
    if args.command == "dashboard-browser-smoke":
        from .dashboard_browser_smoke import run_dashboard_browser_smoke

        payload = run_dashboard_browser_smoke(
            args.url,
            settings.data_dir,
            seconds=args.seconds,
            update_baseline=args.update_baseline,
        )
        print(json.dumps(payload, default=str))
        if payload["status"] != "ok":
            raise SystemExit(1)
        return
    if args.command == "dashboard-operator-evidence":
        from .dashboard_evidence import build_operator_evidence, write_operator_evidence

        payload = build_operator_evidence(
            settings,
            mode=args.mode,
            profile=args.profile,
            source=args.source,
        )
        path = write_operator_evidence(settings, payload)
        print(json.dumps({"path": str(path), **payload}, default=str))
        return
    if args.command.startswith("demo-execution"):
        from .binance import BinanceSpotAdapter
        from .demo_execution_sandbox import DemoExecutionSandbox, intent_from_values

        adapter = BinanceSpotAdapter(settings) if settings.binance_api_key and settings.binance_api_secret else None
        sandbox = DemoExecutionSandbox(settings, adapter=adapter)
        if args.command == "demo-execution-preview":
            result = sandbox.preview(intent_from_values(args.symbol, args.side, args.quote_size, args.last_price))
        elif args.command == "demo-execution-test-order":
            result = sandbox.test_order_only(intent_from_values(args.symbol, args.side, args.quote_size, args.last_price))
        elif args.command == "demo-execution-place":
            result = sandbox.place_demo_order(
                intent_from_values(args.symbol, args.side, args.quote_size, args.last_price),
                confirm_demo_order=args.confirm_demo_order,
                armed=args.armed,
            )
        elif args.command == "demo-execution-query":
            result = sandbox.query_order(
                args.symbol,
                order_id=args.order_id or None,
                client_order_id=args.client_order_id or None,
            )
        elif args.command == "demo-execution-cancel":
            result = sandbox.cancel_order(args.symbol, args.order_id, confirm_cancel=args.confirm_cancel)
        else:
            print(json.dumps(sandbox.latest_report(), default=str))
            return
        print(json.dumps(result.to_dict(), default=str))
        if result.status == "BLOCKED" and args.command in {"demo-execution-place", "demo-execution-cancel"}:
            raise SystemExit(1)
        return
    if args.command == "dashboard":
        command = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "src/binance_spot_bot/ui/streamlit_app.py",
            "--",
            "--mode",
            args.mode,
            "--symbol",
            args.symbol,
            "--interval",
            args.interval,
            "--source",
            args.source,
        ]
        print(" ".join(command))
        return


def _default_limits() -> RiskLimits:
    return RiskLimits(
        max_daily_loss_quote=Decimal("50"),
        max_position_quote=Decimal("25"),
        max_trades_per_day=5,
        min_signal_confidence=0.1,
        max_spread_bps=Decimal("20"),
    )


def _runtime_summary(payload: dict) -> dict:
    return {
        "mode": payload["mode"],
        "symbol": payload["symbol"],
        "status": payload["status"],
        "message": payload["message"],
        "source": payload["market_data"]["source"],
        "session_id": payload["session_id"],
        "equity": str(payload["equity"]),
        "paper_position": str(payload["paper_position"]),
        "signals": payload["metrics"]["signals"],
        "block_reasons": payload["metrics"]["block_reasons"],
        "fills": len(payload["fills"]),
        "data_quality": payload["data_quality"]["status"],
        "active_model": payload["active_model"].get("model_version"),
        "exchange_profile": payload.get("exchange_profile", {}).get("name"),
        "demo_trading_armed": payload.get("demo_connection", {}).get("armed", False),
        "demo_pilot": payload.get("demo_pilot", {}).get("config", {}).get("pilot_name"),
        "reconciliation": payload.get("reconciliation", {}).get("status"),
    }


def _load_or_demo_candles(settings: BotSettings, symbol: str, interval: str, scenario: str):
    datastore = DataStore(settings.data_dir)
    try:
        return datastore.load_candles_csv(symbol, interval)
    except FileNotFoundError:
        return DemoMarketReplay(symbol=symbol, scenario=scenario, count=160).candles()


def _csv_arg(value: str) -> list[str]:
    return [item.strip().upper() for item in value.split(",") if item.strip()]


def _demo_klines() -> list[list[str | int]]:
    rows: list[list[str | int]] = []
    price = Decimal("100")
    for i in range(40):
        open_price = price
        close = price + Decimal(i % 5 - 2) / Decimal("10")
        high = max(open_price, close) + Decimal("0.2")
        low = min(open_price, close) - Decimal("0.2")
        rows.append(
            [
                i * 60_000,
                str(open_price),
                str(high),
                str(low),
                str(close),
                "10",
                i * 60_000 + 59_999,
                "1000",
                10,
                "5",
                "500",
                "0",
            ]
        )
        price = close
    return rows


if __name__ == "__main__":
    main()

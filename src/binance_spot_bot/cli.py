from __future__ import annotations

import argparse
import json
import sys
import time
from decimal import Decimal
from pathlib import Path

from .audit import AuditLog
from .backtest import BacktestEngine
from .config import BotSettings
from .connectivity import connectivity_report
from .check_all import payload_for, print_payload, run_checks
from .control_center import start_control_center
from .data import DataStore, parse_binance_klines
from .data_quality import check_candles
from .demo import DemoMarketReplay
from .diagnostics import collect_diagnostics
from .evaluation import WalkForwardConfig, evaluate_rule_baseline, evaluate_walk_forward, report_to_dict
from .experiment_db import ExperimentDB
from .features import build_feature_rows, build_label_rows
from .launcher import find_free_port
from .model_registry import ModelRegistry
from .pilot_orchestrator import DemoPilotOrchestrator, PilotRunStore
from .pilot_runner import PilotRunnerService, start_background_runner
from .preflight import run_preflight
from .risk import RiskEngine, RiskLimits
from .runtime import BotRuntime, RuntimeOptions, snapshot_to_dict
from .security import scan_for_secrets
from .session_report import export_session_report
from .session_store import SessionStore
from .signal_model import TinyNeuralSignalModel
from .support_bundle import create_support_bundle


def main() -> None:
    parser = argparse.ArgumentParser(prog="spot-bot")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate-config")
    sub.add_parser("preflight")
    sub.add_parser("diagnostics")
    support_bundle = sub.add_parser("support-bundle")
    support_bundle.add_argument("--output", default="")
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
        print(json.dumps(collect_diagnostics(settings).to_dict(), default=str))
        return
    if args.command == "support-bundle":
        output = Path(args.output) if args.output else settings.data_dir / "support" / "support-bundle.zip"
        print(json.dumps(create_support_bundle(settings, output), default=str))
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

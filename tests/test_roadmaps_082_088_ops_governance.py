from __future__ import annotations

from decimal import Decimal

from binance_spot_bot.action_center import create_reviewed_action, propose_action
from binance_spot_bot.config import BotSettings
from binance_spot_bot.disaster_recovery_drills import run_disaster_recovery_drill
from binance_spot_bot.local_ops_automation import generate_scheduled_ops_report
from binance_spot_bot.metrics_warehouse import write_metrics_report
from binance_spot_bot.ops_assistant import answer_ops_question
from binance_spot_bot.permission_profiles import evaluate_permission, permission_compliance_report
from binance_spot_bot.policy_rollout import (
    PaperPolicyVariant,
    assign_ab_bucket,
    create_policy_experiment,
    evaluate_champion_challenger,
    policy_rollout_report,
)
from binance_spot_bot.types import TradingMode


def _settings(tmp_path):
    return BotSettings(
        app_env="local",
        trading_mode=TradingMode.DISABLED,
        binance_base_url="https://api.binance.com",
        binance_testnet_base_url="https://testnet.binance.vision",
        binance_api_key="",
        binance_api_secret="",
        live_trading_enabled=False,
        kill_switch=True,
        manual_live_approval="",
        max_daily_loss_quote=Decimal("50"),
        max_position_quote=Decimal("25"),
        max_trades_per_day=5,
        min_signal_confidence=0.2,
        max_spread_bps=Decimal("20"),
        data_dir=tmp_path / "data",
        audit_log_path=tmp_path / "data" / "audit" / "events.jsonl",
    )


def test_082_policy_rollout_ab_champion_challenger_report(tmp_path):
    settings = _settings(tmp_path)
    experiment = create_policy_experiment(
        PaperPolicyVariant("champion", "champion", "balanced", 3, 0.35),
        PaperPolicyVariant("challenger", "candidate", "conservative", 4, 0.25),
        ["btcusdt", "ethusdt"],
        traffic_split_pct=50,
        min_observations=1,
    )
    variant = assign_ab_bucket("BTCUSDT", experiment.experiment_id, 50)
    evaluation = evaluate_champion_challenger(
        experiment,
        [
            {"symbol": "BTCUSDT", "variant": variant, "pnl": "1.0", "drawdown": "0.1"},
            {"symbol": "ETHUSDT", "variant": "champion", "pnl": "0.2", "drawdown": "0.1"},
        ],
    )
    report = policy_rollout_report(settings, experiment, evaluation)

    assert report["evaluation"]["decision"] in {"keep_champion", "promote_challenger", "rollback_challenger"}
    assert report["evaluation"]["live_trading_enabled"] is False
    assert (settings.data_dir / "paper-policy-rollouts" / "latest-policy-rollout.json").exists()


def test_083_local_ops_automation_writes_schedule_and_runbook(tmp_path):
    settings = _settings(tmp_path)
    report = generate_scheduled_ops_report(settings)

    assert report["schedule"]["status"] == "ready"
    assert report["live_trading_enabled"] is False
    assert (settings.data_dir / "local-ops" / "automation" / "operator-runbook.md").exists()


def test_084_metrics_warehouse_aggregates_and_flags_anomalies(tmp_path):
    settings = _settings(tmp_path)
    report = write_metrics_report(
        settings,
        [{"equity": 1000, "pnl_quote": 1.5, "latency_ms": 20}, {"equity": 999, "pnl_quote": -0.5, "latency_ms": 30}],
    )

    assert report["rows"] == 2
    assert report["metrics"]["latency_ms"]["avg"] == 25
    assert report["live_trading_enabled"] is False


def test_085_ops_assistant_answers_status_and_blocks_trading_intents(tmp_path):
    settings = _settings(tmp_path)
    answer = answer_ops_question(settings, "Wat is de bot status?")
    blocked = answer_ops_question(settings, "place order market buy BTC")

    assert answer["status"] == "answered"
    assert answer["sources"]
    assert blocked["status"] == "blocked"
    assert blocked["live_trading_enabled"] is False


def test_086_action_center_requires_approval_and_blocks_unsafe_actions(tmp_path):
    settings = _settings(tmp_path)
    approved = create_reviewed_action(settings, "export_report", "daily report", approved=True)
    unsafe = propose_action("withdraw", "not allowed")

    assert approved["review"]["status"] == "approved_waiting_execution"
    assert approved["execution"]["requires_manual_click"] is True
    assert unsafe.status == "blocked_unsafe_action"


def test_087_permission_profiles_block_live_trading_and_write_compliance(tmp_path):
    settings = _settings(tmp_path)
    allowed = evaluate_permission("operator", "start_demo")
    blocked = evaluate_permission("operator", "live_trade")
    report = permission_compliance_report(settings)

    assert allowed["allowed"] is True
    assert blocked["allowed"] is False
    assert report["status"] == "ok"
    assert report["matrix"]["live_trading_enabled"] is False


def test_088_disaster_recovery_drill_archives_and_scans_state(tmp_path):
    settings = _settings(tmp_path)
    settings.data_dir.mkdir(parents=True)
    (settings.data_dir / "sample.json").write_text('{"ok": true}', encoding="utf-8")

    report = run_disaster_recovery_drill(settings)

    assert report["status"] in {"pass", "warn"}
    assert report["integrity"]["checked"] >= 1
    assert report["live_trading_enabled"] is False
    assert (settings.data_dir / "disaster-recovery" / "latest-dr-drill.json").exists()

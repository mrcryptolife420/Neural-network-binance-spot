from __future__ import annotations

from dataclasses import replace

from binance_spot_bot.app_control import LIVE_ARM_CONFIRM
from binance_spot_bot.app_control.app_evidence import export_app_control_evidence
from binance_spot_bot.app_control.app_supervisor import app_supervisor_plan
from binance_spot_bot.app_control.bot_profile import BotProfile, BotProfileMode, built_in_profiles, validate_bot_profile
from binance_spot_bot.app_control.config_wizard import create_profile_from_wizard
from binance_spot_bot.app_control.data_bootstrap import data_bootstrap_report
from binance_spot_bot.app_control.one_click_launcher import generate_one_click_launcher
from binance_spot_bot.app_control.profile_matrix import profile_matrix_report
from binance_spot_bot.app_control.profile_store import default_profile_store
from binance_spot_bot.app_control.runtime_orchestrator import start_profile
from binance_spot_bot.app_control.secret_refs import secret_ref_status
from binance_spot_bot.app_control.startup_health import startup_health_report
from binance_spot_bot.live_training.demo_dataset_quality import evaluate_demo_dataset_quality
from binance_spot_bot.live_training.demo_spot_data_recorder import record_demo_spot_events
from binance_spot_bot.live_training.live_readiness_gate import evaluate_live_readiness_gate
from binance_spot_bot.live_training.live_training_evidence import export_live_training_evidence
from binance_spot_bot.live_training.model_validation_gate import evaluate_model_validation_gate
from binance_spot_bot.live_training.training_dataset_builder import build_training_dataset


def test_profile_schema_blocks_live_auto_start_raw_secret_and_unsafe_values() -> None:
    paper = next(item for item in built_in_profiles() if item.mode == BotProfileMode.PAPER.value)
    assert validate_bot_profile(paper).status == "ok"
    live = next(item for item in built_in_profiles() if item.mode == BotProfileMode.LIVE_LOCKED.value)
    assert validate_bot_profile(live).status == "ok"
    assert validate_bot_profile(replace(live, auto_start_runtime=True)).status == "blocked"
    assert validate_bot_profile(replace(live, training_gate=replace(live.training_gate, required_dataset_quality_score=0))).status == "blocked"
    assert validate_bot_profile(replace(paper, description="guaranteed profit")).status == "blocked"
    assert validate_bot_profile(replace(paper, base_url="https://evil.example")).status == "blocked"
    assert validate_bot_profile(replace(paper, symbol="bad-symbol")).status == "blocked"
    raw_secret = "A" * 64
    assert validate_bot_profile(replace(paper, description=raw_secret)).status == "blocked"


def test_profile_store_wizard_secret_refs_supervisor_launcher_and_runtime(tmp_path) -> None:
    store = default_profile_store(tmp_path)
    assert store.validate_all()["status"] == "ok"
    wizard = create_profile_from_wizard("demo_spot", "ETHUSDT")
    assert wizard["status"] == "ok"
    assert secret_ref_status()["raw_secret_visible"] is False
    supervisor = app_supervisor_plan(tmp_path)
    assert supervisor["live_auto_start"] is False
    launcher = generate_one_click_launcher(tmp_path)
    assert launcher["status"] == "ok"
    assert "Start-Neural-Binance-Bot.cmd" in launcher["files"]["cmd"]
    paper = next(item for item in built_in_profiles() if item.mode == BotProfileMode.PAPER.value)
    assert data_bootstrap_report(paper)["live_order_action"] is False
    assert start_profile(paper)["state"] == "running"
    live = next(item for item in built_in_profiles() if item.mode == BotProfileMode.LIVE_LOCKED.value)
    assert start_profile(live)["status"] == "blocked"
    assert startup_health_report(tmp_path)["live_trading_enabled"] is False
    assert profile_matrix_report()["status"] == "ok"


def test_demo_training_dataset_model_gate_live_readiness_and_evidence(tmp_path) -> None:
    recording = record_demo_spot_events(tmp_path)
    quality = evaluate_demo_dataset_quality(recording)
    assert quality["status"] == "ok"
    dataset = build_training_dataset(tmp_path, recording, quality)
    assert dataset["status"] == "ok"
    validation = evaluate_model_validation_gate(dataset)
    assert validation["status"] == "ok"
    live = next(item for item in built_in_profiles() if item.mode == BotProfileMode.LIVE_LOCKED.value)
    readiness = evaluate_live_readiness_gate(live, validation)
    assert readiness["status"] == "ready_to_arm"
    evidence = export_live_training_evidence(tmp_path, recording, quality, dataset, validation)
    assert evidence["manifest"]["no_raw_secret_proof"] is True
    app_evidence = export_app_control_evidence(tmp_path, {"run_id": "acceptance", "validation": validation, "live_trading_enabled": False})
    assert app_evidence["manifest"]["launcher_never_auto_starts_live"] is True


def test_live_arm_confirm_constant_and_execution_gate_remains_blocked() -> None:
    assert LIVE_ARM_CONFIRM == "I_UNDERSTAND_LIVE_SPOT_TRADING_RISK"
    armed = BotProfile("live-armed", "Live Armed", "test", BotProfileMode.LIVE_ARMED.value, training_gate=next(item for item in built_in_profiles() if item.mode == BotProfileMode.LIVE_LOCKED.value).training_gate)
    assert start_profile(armed)["status"] == "blocked"


def test_dashboard_v2_control_center_api_smoke() -> None:
    try:
        from fastapi.testclient import TestClient
    except Exception:
        return
    from binance_spot_bot.dashboard_v2.app import create_dashboard_v2_app

    client = TestClient(create_dashboard_v2_app())
    assert client.get("/api/app-control/health").json()["live_trading_enabled"] is False
    assert client.get("/api/app-control/profiles").json()["status"] == "ok"
    assert client.post("/api/app-control/runtime/start").json()["live_trading_enabled"] is False


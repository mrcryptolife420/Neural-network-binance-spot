from __future__ import annotations

import json

from binance_spot_bot.live_training.demo_dataset_quality_v2 import evaluate_demo_dataset_quality_v2
from binance_spot_bot.live_training.demo_dataset_vault import ingest_demo_vault
from binance_spot_bot.live_training.demo_session_targets import (
    calculate_demo_session_target_progress,
    default_demo_session_target,
    fixture_complete_sessions,
)
from binance_spot_bot.live_training.demo_spot_data_recorder import record_demo_spot_events
from binance_spot_bot.live_training.demo_to_live_pipeline import run_demo_to_live_pipeline
from binance_spot_bot.live_training.feature_label_dataset import build_feature_label_dataset_v2
from binance_spot_bot.live_training.live_candidate_gate import evaluate_live_candidate_gate
from binance_spot_bot.live_training.model_candidate_registry import create_model_candidate, validate_candidate_transition
from binance_spot_bot.live_training.model_strategy_validation import run_model_strategy_validation
from binance_spot_bot.live_training.paper_replay_from_demo import run_paper_replay_from_demo
from binance_spot_bot.live_training.split_governance import evaluate_split_governance
from binance_spot_bot.live_training.testnet_promotion_gate import evaluate_testnet_promotion_gate
from binance_spot_bot.live_training.testnet_rehearsal_runner import TESTNET_REHEARSAL_CONFIRM, run_testnet_rehearsal


def test_demo_session_targets_cover_complete_partial_live_and_redaction() -> None:
    target = default_demo_session_target()
    empty = calculate_demo_session_target_progress(target, [])
    assert empty["status"] == "blocked"
    assert "demo collection targets incomplete" in empty["blockers"]
    assert empty["live_trading_enabled"] is False
    assert empty["live_execution_enabled"] is False
    assert "FINANCIAL ADVICE" in empty["not_financial_advice_statement"]

    complete = calculate_demo_session_target_progress(target, fixture_complete_sessions())
    assert complete["status"] == "ok"
    assert complete["progress_percent"] == 100.0
    assert complete["missing_targets"] == []
    assert complete["missing_market_regimes"] == []

    contaminated = calculate_demo_session_target_progress(target, [{"mode": "live", "runtime_minutes": 1, "api_secret": "A" * 64}])
    assert contaminated["status"] == "blocked"
    assert "live event contamination" in contaminated["blockers"]
    assert "session missing runtime_minutes" not in contaminated["warnings"]
    assert "A" * 64 not in json.dumps(contaminated)

    warning = calculate_demo_session_target_progress(target, [{"session_id": "missing-runtime"}])
    assert "session missing runtime_minutes" in warning["warnings"]


def test_demo_to_live_pipeline_promotes_only_to_testnet_rehearsal_and_keeps_live_locked(tmp_path) -> None:
    pipeline = run_demo_to_live_pipeline(tmp_path)
    assert pipeline["target"]["status"] == "ok"
    assert pipeline["quality"]["grade"] in {"A", "B"}
    assert pipeline["validation"]["status"] == "ok"
    assert pipeline["paper_replay"]["status"] == "ok"
    assert pipeline["testnet_promotion"]["state"] == "ready_for_testnet_rehearsal"
    assert pipeline["testnet_rehearsal"]["status"] == "ok"
    assert pipeline["live_candidate"]["status"] == "blocked"
    assert pipeline["live_candidate"]["live_execution_enabled"] is False
    assert pipeline["live_trading_enabled"] is False
    assert pipeline["evidence"]["manifest"]["no_secret_proof"] is True


def test_live_training_components_block_low_quality_and_require_confirm(tmp_path) -> None:
    target = calculate_demo_session_target_progress(default_demo_session_target(), [])
    recording = record_demo_spot_events(tmp_path)
    vault = ingest_demo_vault(tmp_path, [recording])
    burndown = {"status": "warn", "issues": [{"priority": "DQ-P1", "category": "too few sessions"}]}
    quality = evaluate_demo_dataset_quality_v2(vault, target, burndown)
    assert quality["status"] == "blocked"
    assert quality["grade"] in {"D", "F"}

    dataset = build_feature_label_dataset_v2(tmp_path, vault, quality)
    split = evaluate_split_governance(dataset)
    candidate = create_model_candidate(dataset)
    validation = run_model_strategy_validation(candidate, quality, split)
    replay = run_paper_replay_from_demo(dataset, validation)
    promotion = evaluate_testnet_promotion_gate(target, quality, validation, replay)
    assert promotion["status"] == "blocked"

    assert run_testnet_rehearsal(promotion)["status"] == "blocked"
    assert run_testnet_rehearsal({"status": "ok"}, confirm=TESTNET_REHEARSAL_CONFIRM, base_url="https://api.binance.com/api")["status"] == "blocked"

    live_candidate = evaluate_live_candidate_gate({"manifest": {}}, {"status": "blocked"})
    assert live_candidate["live_trading_enabled"] is False
    assert "evidence hashes required" in live_candidate["blockers"]


def test_model_candidate_state_machine_blocks_gate_skips() -> None:
    assert validate_candidate_transition("draft", "dataset_ready")["status"] == "ok"
    assert validate_candidate_transition("dataset_ready", "testnet_passed")["status"] == "blocked"

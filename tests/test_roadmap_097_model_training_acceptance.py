from __future__ import annotations

import json

from binance_spot_bot.inference_checks import inference_compatibility_check, inference_latency_budget
from binance_spot_bot.local_experiment_tracker import LocalExperimentTracker
from binance_spot_bot.model_card_v2 import model_card_v2
from binance_spot_bot.model_promotion_gate import model_promotion_gate
from binance_spot_bot.model_training import synthetic_training_rows, train_tiny_model
from binance_spot_bot.training_config import TrainingDataBinding, TrainingJobConfig, validate_training_config
from binance_spot_bot.training_pipeline import run_training_pipeline
from binance_spot_bot.feature_store_contracts import contract_from_features


def test_training_config_validation_blocks_schema_mismatch_and_live() -> None:
    config = TrainingJobConfig(
        job_id="job-1",
        experiment_name="exp",
        data=TrainingDataBinding("features", "labels", "hash-a"),
    )
    valid = validate_training_config(config, expected_feature_schema_hash="hash-a")
    invalid = validate_training_config(config, expected_feature_schema_hash="hash-b")
    live = validate_training_config(TrainingJobConfig("job-2", "exp", TrainingDataBinding("", "", "hash"), live_trading_enabled=True))

    assert valid["status"] == "ok"
    assert invalid["status"] == "blocked"
    assert "feature_schema_mismatch" in invalid["blockers"]
    assert "live_trading_not_allowed" in live["blockers"]
    assert valid["live_trading_enabled"] is False


def test_local_experiment_tracker_redacts_and_indexes_runs(tmp_path) -> None:
    tracker = LocalExperimentTracker(tmp_path / "experiments")
    run = tracker.start_run("demo", {"api_secret": "abcdefghijklmnopqrstuvwxyz"})
    completed = tracker.complete_run(run, metrics={"score": 0.7}, artifacts={"model": "model.json"})

    assert completed.status == "completed"
    assert len(tracker.list_runs()) == 1
    assert "[REDACTED]" in (tmp_path / "experiments" / "experiment-runs.json").read_text(encoding="utf-8")


def test_inference_compatibility_latency_and_model_card() -> None:
    features, labels = synthetic_training_rows(12)
    contract = contract_from_features("dataset", features, lookback_window=5)
    model = train_tiny_model(features, labels, epochs=2)
    compatible = inference_compatibility_check(model, contract)
    latency = inference_latency_budget(model, features[-1], budget_ms=100)
    card = model_card_v2("model-1", {"score": 0.7}, contract.to_dict())

    assert compatible["status"] == "ok"
    assert latency["status"] == "ok"
    assert card["forbidden_use"] == "live trading"
    assert card["live_trading_enabled"] is False


def test_training_pipeline_writes_manifest_evidence_and_blocks_unconfirmed_promotion(tmp_path) -> None:
    blocked = run_training_pipeline(0, root=tmp_path)
    trained = run_training_pipeline(20, root=tmp_path, operator_confirmed=False)
    confirmed = run_training_pipeline(20, root=tmp_path / "confirmed", operator_confirmed=True)

    assert blocked["status"] == "blocked"
    assert trained["status"] == "ok"
    assert trained["promotion"]["status"] == "blocked"
    assert "operator_confirmed" in trained["promotion"]["blockers"]
    assert confirmed["promotion"]["status"] == "ok"
    assert confirmed["promotion"]["scope"] == "paper_shadow_demo_only"
    assert confirmed["artifact_manifest"]["artifact_sha256"]
    assert json.loads((tmp_path / "confirmed" / "experiments" / "experiment-runs.json").read_text(encoding="utf-8"))[0]["live_trading_enabled"] is False


def test_model_promotion_gate_requires_full_contract() -> None:
    ok = model_promotion_gate(0.7, operator_confirmed=True)
    blocked = model_promotion_gate(0.7, operator_confirmed=True, leakage_pass=False, inference_compatible=False)

    assert ok["status"] == "ok"
    assert blocked["status"] == "blocked"
    assert {"leakage_pass", "inference_compatible"}.issubset(set(blocked["blockers"]))
    assert blocked["live_trading_enabled"] is False

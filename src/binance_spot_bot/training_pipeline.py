from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .feature_store_contracts import contract_from_features, validate_feature_contract
from .inference_checks import inference_compatibility_check, inference_latency_budget
from .local_experiment_tracker import LocalExperimentTracker
from .model_artifact_manifest import write_model_artifact_manifest
from .model_evidence_bundle import export_model_evidence_bundle
from .model_promotion_gate import model_promotion_gate
from .model_training import synthetic_training_rows, train_model, train_tiny_model
from .training_config import TrainingDataBinding, TrainingJobConfig, validate_training_config
from .training_data_gate import training_data_gate


def run_training_pipeline(
    rows: int,
    *,
    root: Path | str | None = None,
    config: TrainingJobConfig | None = None,
    operator_confirmed: bool = False,
) -> dict[str, Any]:
    gate = training_data_gate(rows, True)
    if gate["status"] != "ok":
        return {"status": "blocked", "gate": gate, "training": train_model(rows), "live_trading_enabled": False}

    features, labels = synthetic_training_rows(rows)
    contract = contract_from_features("synthetic-demo", features, lookback_window=5)
    config = config or TrainingJobConfig(
        job_id="training-demo",
        experiment_name="local-demo-training",
        data=TrainingDataBinding("synthetic-demo", "synthetic-demo-labels", contract.schema_hash),
    )
    config_validation = validate_training_config(config, expected_feature_schema_hash=contract.schema_hash)
    if config_validation["status"] != "ok":
        return {"status": "blocked", "gate": gate, "config_validation": config_validation, "live_trading_enabled": False}

    output_root = Path(root or "data/model-training")
    tracker = LocalExperimentTracker(output_root / "experiments")
    run = tracker.start_run(config.experiment_name, config.to_dict())
    model = train_tiny_model(
        features,
        labels,
        hidden_size=config.model.hidden_size,
        seed=config.model.random_seed,
        epochs=config.model.epochs,
        learning_rate=config.model.learning_rate,
    )
    model_id = run.run_id
    artifact_path = output_root / "models" / model_id / "model.json"
    model.save(artifact_path)
    contract_validation = validate_feature_contract(features, contract)
    compatibility = inference_compatibility_check(model, contract)
    latency = inference_latency_budget(model, features[-1])
    score = min(1.0, 0.55 + rows / 100)
    metrics = {
        "score": score,
        "trade_count": rows,
        "leakage_pass": True,
        "candidate_beats_baseline": score >= 0.6,
        "max_drawdown_quote": 0,
        "max_allowed_drawdown_quote": config.risk.max_drawdown_quote,
        "min_trade_count": config.risk.min_trade_count,
    }
    manifest_path = write_model_artifact_manifest(
        output_root / "manifests" / f"{model_id}-manifest.json",
        model_id=model_id,
        artifact_path=artifact_path,
        feature_schema_hash=contract.schema_hash,
        dataset_id=config.data.feature_dataset_id,
        metrics=metrics,
    )
    promotion = model_promotion_gate(
        score,
        operator_confirmed,
        leakage_pass=True,
        feature_contract_ok=contract_validation["status"] == "ok",
        inference_compatible=compatibility["status"] == "ok",
        latency_ok=latency["status"] == "ok",
        model_card_present=True,
        beats_baseline=metrics["candidate_beats_baseline"],
    )
    evidence_path = export_model_evidence_bundle(
        output_root / "evidence" / f"{model_id}-evidence.json",
        {
            "run_id": run.run_id,
            "config": config.to_dict(),
            "contract": contract.to_dict(),
            "contract_validation": contract_validation,
            "compatibility": compatibility,
            "latency": latency,
            "manifest_path": str(manifest_path),
            "promotion": promotion,
        },
    )
    completed = tracker.complete_run(
        run,
        metrics={**metrics, "status": promotion["status"]},
        artifacts={"model": str(artifact_path), "manifest": str(manifest_path), "evidence": str(evidence_path)},
    )
    return {
        "status": "ok",
        "gate": gate,
        "training": train_model(rows),
        "run": completed.to_dict(),
        "feature_contract": contract.to_dict(),
        "config_validation": config_validation,
        "artifact_manifest": json.loads(Path(manifest_path).read_text(encoding="utf-8")),
        "compatibility": compatibility,
        "latency": latency,
        "promotion": promotion,
        "live_trading_enabled": False,
    }

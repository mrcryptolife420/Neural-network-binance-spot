# Model Training Safety Contract

Roadmap: 097

Model training is local-only and may promote models only for paper, shadow or demo use.

Rules:
- No live trading.
- No signed order endpoints.
- No account endpoints.
- Training requires dataset/feature contracts.
- Promotion requires leakage pass, compatible feature schema, model card, latency check, baseline comparison and operator confirmation.
- Artifacts, experiment runs and evidence bundles are redacted.
- Promotion scope is `paper_shadow_demo_only`.

Validation:
- `TrainingJobConfig` validates schema and no-live settings.
- `LocalExperimentTracker` stores redacted local run history.
- `run_training_pipeline` writes model, manifest and evidence artifacts.
- `model_promotion_gate` blocks unconfirmed or incompatible candidates.

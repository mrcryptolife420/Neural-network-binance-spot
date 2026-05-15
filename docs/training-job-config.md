# Training Job Config

Roadmap: 097

`training_config.py` defines:
- `TrainingJobConfig`
- `TrainingDataBinding`
- `TrainingModelSpec`
- `TrainingSplitPolicy`
- `TrainingCostAssumptions`
- `TrainingRiskAssumptions`
- `TrainingValidationPolicy`

The config is JSON-serializable and redacted. It blocks live-enabled jobs, missing datasets, missing manifests, schema mismatches and invalid hyperparameters.

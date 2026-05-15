# Local Experiment Tracker

Roadmap: 097

`LocalExperimentTracker` writes local run JSON and an index file. It records:
- run id
- experiment name
- config
- metrics
- artifacts
- no-live proof

It is deliberately filesystem-only and does not send telemetry.

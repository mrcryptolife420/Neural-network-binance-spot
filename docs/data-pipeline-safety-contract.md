# Data Pipeline Safety Contract

Roadmap: 096

The data pipeline is local-first and may use public market data only. It must not use signed account/order endpoints and must not enable live trading.

Rules:
- Dataset manifests and evidence are redacted.
- Paths must stay inside the configured data root.
- Artifacts use an allowlisted suffix.
- Feature/label computation is deterministic.
- Feature contracts include schema hashes and generator versions.
- Data quality failures produce warnings/evidence, not trading actions.
- Cache cleanup remains outside this roadmap and requires preview/confirm.

Validation:
- `DataStoreRoot` enforces path policy and writes artifact hashes.
- `FeatureStoreContract` validates schema hash.
- `IncrementalFeatureBuilder` reuses existing feature logic.
- `data_pipeline_evidence` exports quality and lineage with `live_trading_enabled=false`.

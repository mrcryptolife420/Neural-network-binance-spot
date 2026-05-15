# Feature Store Contracts

Roadmap: 096

`feature_store_contracts.py` wraps existing feature generation with a stable schema contract.

Contract fields:
- dataset id
- schema hash
- feature names
- generator version
- lookback window

The contract is designed for runtime, evaluation and future model training reuse.

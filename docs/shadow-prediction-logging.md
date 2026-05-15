# Shadow Prediction Logging

Roadmap: 098

`log_shadow_prediction` writes redacted local JSONL rows with model alias, symbol, prediction and optional features.

The logger is append-only and does not invoke execution or order APIs.

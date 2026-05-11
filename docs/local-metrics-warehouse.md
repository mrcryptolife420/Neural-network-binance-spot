# Local Metrics Warehouse

The metrics warehouse writes append-only JSONL under `data/metrics-warehouse/metrics.jsonl`. It supports append, append many, query, latest, series, daily aggregation, weekly aggregation, manifest writing, manifest verification, and confirm-gated compaction.

The warehouse has no database dependency and stores redacted local metrics only.

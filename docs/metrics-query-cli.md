# Metrics Query CLI

Metrics commands:

- `metrics-ingest --source all`
- `metrics-query --name <metric> --days 7`
- `metrics-latest --category health`
- `metrics-aggregate --daily`
- `metrics-slo`
- `metrics-anomalies`
- `metrics-export --days 30`
- `metrics-compact --older-than-days 30 --confirm COMPACT_METRICS`

Commands work without API keys and keep live trading disabled.

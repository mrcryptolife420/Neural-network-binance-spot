# Metrics Event Schema

`MetricEvent` is the canonical observability event. It includes event id, timestamp, source, category, metric name, value, unit, status, severity, labels, artifact path, evidence id, schema version, redaction flag, and `live_trading_enabled: false`.

Supported categories include job, scheduler, report, health, check, dashboard, session, paper performance, portfolio, governance, support, storage, evidence, data quality, and incident.

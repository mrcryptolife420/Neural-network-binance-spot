# Local Observability Safety Contract

Metrics and analytics are local-only. Collectors are read-only and must not call Binance signed, account, order, or live endpoints.

Rules:

- no remote telemetry
- no cloud upload
- no API secrets in labels or metric values
- no live mode
- no automatic trading actions from anomalies or SLO breaches
- reports and bundles are redacted
- recommendations may point to runbooks or support bundles only

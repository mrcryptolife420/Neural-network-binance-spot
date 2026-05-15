# Performance Profiling Safety Contract

- Profiling is local-only.
- No remote telemetry or uploads.
- No live trading, signed endpoints, account endpoints, or order endpoints.
- Profiling wrappers measure timing/resource data without changing business logic.
- Reports must be redacted and secret-free.
- Live trading enabled: false.

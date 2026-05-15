# Dashboard Refactor Safety Contract

Roadmap: 094

The Streamlit dashboard remains a local operator UI. Refactors may improve page structure, payload limits, lazy loading and smoke coverage, but must not add live trading capability.

Rules:
- `LIVE TRADING DISABLED` remains visible in the app shell.
- `SELECTABLE_MODES` must not include `live`.
- Page registry entries must keep `live_trading_enabled=false`.
- Page modules are lazy metadata boundaries; runtime business logic stays in existing runtime/services.
- Debug payloads are redacted and size-limited.
- Table payloads are row-limited.
- Chart keys must be stable and unique.
- Performance budgets can warn operators, but must never start trading actions.
- Browser smoke remains required for critical pages; HTTP fallback is allowed when Windows blocks Playwright subprocess pipes.

Validation:
- `dashboard_smoke_v2()` validates registry, stable chart keys, payload limits and no-live mode.
- `dashboard-smoke` validates import/render contract.
- `check-all --skip-tests` validates preflight, secret scan, dashboard import and no-live UI checks.

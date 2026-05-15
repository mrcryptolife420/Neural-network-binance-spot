# Runtime Snapshot Profiles

Roadmap: 095

Snapshot profiles:
- `compact`: identity, lifecycle, model and safety.
- `dashboard`: dashboard-facing runtime state.
- `full`: broad local diagnostic payload.
- `evidence`: audit/report oriented payload.

All profiles return:
- `kind=runtime_snapshot`
- `profile`
- limited/redacted `payload`
- `live_trading_enabled=false`

# Dashboard V2 Customization Safety Contract

Dashboard V2 workspace customization is local-only and cannot enable live trading.

Rules:

- Layouts, preferences, watchlists and evidence stay on the local machine.
- No remote telemetry, cloud layout sync or arbitrary plugin code is allowed.
- Supported modes are demo, paper and testnet-readiness only.
- `live_trading_enabled` must always be `false`.
- The no-live banner and operator stop control are mandatory in operator workspaces.
- Safety widgets are locked and cannot be hidden by layout import.
- Widget types are allowlisted by `dashboard_v2.widget_registry`.
- Imports reject live modes, unknown widgets, script content and unsafe paths.
- Exports and evidence use redaction before writing JSON or Markdown.
- Reports must include the no-live statement.

Validation entrypoints:

- `python -m binance_spot_bot.cli dashboard-v2-workspace-presets --json`
- `python -m binance_spot_bot.cli dashboard-v2-widget-registry --json`
- `python -m binance_spot_bot.cli dashboard-v2-workspace-validate --workspace <id> --json`
- `python -m binance_spot_bot.cli dashboard-v2-workspace-evidence-export --workspace <id> --json`

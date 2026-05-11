# Dashboard Troubleshooting

Start with:

```powershell
spot-bot dashboard-smoke --seconds 10
spot-bot check-all --json
```

Common checks:

- If the dashboard fails on import, verify Python 3.12+ and UI dependencies.
- If charts fail, run the roadmap 023 stability tests.
- If tabs appear out of order, inspect `binance_spot_bot.ui.page_registry`.
- If demo trading controls are unavailable, confirm Demo Spot credentials are loaded and the operator explicitly armed demo trading.
- Live trading is intentionally disabled.

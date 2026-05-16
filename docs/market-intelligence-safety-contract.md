# Market Intelligence Safety Contract

Roadmap 112 adds a local Market Intelligence Workbench for Binance Spot public market data research.

Rules:

- Live trading remains disabled.
- Scanner code may only use unsigned public market data endpoints.
- Signed, account, user-data, order, cancel, listen-key, and execution endpoints are blocked.
- Scanner rankings are research metrics, not financial advice.
- Scanner output must not trigger autonomous orders.
- Reports and logs must be redacted before writing to disk.
- The workbench must run without API keys.

Primary no-live statement:

```text
MARKET INTELLIGENCE - NO LIVE TRADING
```

Primary public-data statement:

```text
PUBLIC UNSIGNED BINANCE SPOT MARKET DATA ONLY
```

Validation commands:

```powershell
python -m binance_spot_bot.cli market-intelligence-policy --json
python -m binance_spot_bot.cli dashboard-v2-market-intelligence-smoke --json
python -m binance_spot_bot.cli check-all --skip-tests --json
```

# Market Snapshot Cache

The snapshot cache stores local market snapshots for ticker, bookTicker, and kline-shaped payloads.

The cache is local-first and can seed deterministic demo snapshots, so scanner development and tests do not require credentials.

CLI:

```powershell
python -m binance_spot_bot.cli market-snapshot-cache-report --json
```

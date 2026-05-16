# Symbol Universe

The symbol universe builds a local, filterable view of Binance Spot symbols from exchangeInfo-shaped data.

Default behavior:

- quote asset defaults to `USDT`;
- status must be trading;
- filters retain price, quantity, and notional metadata;
- payloads include no API keys and no account state.

CLI:

```powershell
python -m binance_spot_bot.cli symbol-universe-refresh --quote USDT --json
python -m binance_spot_bot.cli symbol-universe-report --json
```

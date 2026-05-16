# Live Order Preview

Order preview computes symbol, side, type, quote size, quantity, price, spread, fees, slippage, expiration, and preview hash.

Preview cannot place an order and must be rebuilt if market/profile inputs change.

Use:

```powershell
python -m binance_spot_bot.cli live-order-preview --json
```

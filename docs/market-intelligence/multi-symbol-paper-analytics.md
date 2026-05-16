# Multi-Symbol Paper Analytics

Multi-symbol paper analytics compares fixture-based paper-only outcomes across a watchlist.

It records candle count, signal count, fills, estimated fees, paper PnL, and drawdown per symbol.

It does not place, test, cancel, or query orders.

CLI:

```powershell
python -m binance_spot_bot.cli multi-symbol-paper-analytics-preview --watchlist majors --json
python -m binance_spot_bot.cli multi-symbol-paper-analytics-run --watchlist majors --confirm RUN_PAPER_ANALYTICS_ONLY --json
```

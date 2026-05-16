# Watchlist Scanner

The watchlist scanner evaluates a preset symbol list using local cached or fixture market snapshots.

It produces:

- per-symbol last price, bid, ask, spread, volume, and 24h change;
- market metrics;
- data quality warnings;
- a local scan-run JSON report.

CLI:

```powershell
python -m binance_spot_bot.cli watchlist-scan-preview --preset majors_overview --json
python -m binance_spot_bot.cli watchlist-scan-run --preset majors_overview --confirm RUN_PUBLIC_MARKET_SCAN --json
```

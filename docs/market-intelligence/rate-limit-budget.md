# Rate Limit Budget

The scanner creates a request budget before it runs a watchlist.

The default budget protects local scans from accidental endpoint bursts by estimating request weight from symbol count and scanner actions.

CLI:

```powershell
python -m binance_spot_bot.cli scanner-rate-limit-plan --preset majors_overview --json
```

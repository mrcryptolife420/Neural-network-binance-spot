# Live Candidate Gate

The live candidate gate checks whether enough evidence exists for a manual live-readiness review.

It never enables live orders. Current output must keep:

- `live_execution_enabled=false`
- `live_trading_enabled=false`
- blocker `live execution implementation gate required`

Use:

```powershell
python -m binance_spot_bot.cli live-candidate-check --json
```

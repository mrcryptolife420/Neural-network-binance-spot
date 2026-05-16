# AI Doctor Summary

## Main status
Local debug bundle generated with safe env.

## Most likely cause
ModuleNotFoundError (confidence: high)

## Suspect files
- src/binance_spot_bot/cli.py
- src/binance_spot_bot/dashboard_v2/app.py

## Recommended tests
- `python -m compileall -q src tests`
- `pytest -q`

## Safety state
- LIVE_TRADING_ENABLED=false
- KILL_SWITCH=true
- No live order path touched
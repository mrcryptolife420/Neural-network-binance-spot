@echo off
set LIVE_TRADING_ENABLED=false
set KILL_SWITCH=true
python -m binance_spot_bot.cli package-rollback-preview --json

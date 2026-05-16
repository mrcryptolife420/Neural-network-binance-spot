@echo off
set LIVE_TRADING_ENABLED=false
set KILL_SWITCH=true
set PYTHONPATH=%CD%\src
python -m binance_spot_bot.cli dashboard-v2

@echo off
setlocal
cd /d "%~dp0"
set LIVE_TRADING_ENABLED=false
set KILL_SWITCH=true
set PYTHONPATH=%CD%\src
python -m binance_spot_bot.cli dashboard-v2-static-verify --json
python -m binance_spot_bot.cli ai-doctor-export --json
pause

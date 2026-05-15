@echo off
set LIVE_TRADING_ENABLED=false
set KILL_SWITCH=true
cd /d "C:\Users\highlife\Desktop\Neural network binance spot"
echo LOCAL REALTIME DASHBOARD - NO LIVE TRADING
"C:\Python314\python.exe" -m binance_spot_bot.cli dashboard-v2 --host 127.0.0.1 --port 8800 --find-free-port

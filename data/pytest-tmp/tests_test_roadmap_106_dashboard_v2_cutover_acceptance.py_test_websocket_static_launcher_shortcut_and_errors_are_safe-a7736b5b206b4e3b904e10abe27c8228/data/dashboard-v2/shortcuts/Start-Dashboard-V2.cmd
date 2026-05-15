@echo off
set LIVE_TRADING_ENABLED=false
set KILL_SWITCH=true
cd /d "C:\Users\highlife\Desktop\Neural network binance spot\data\pytest-tmp\tests_test_roadmap_106_dashboard_v2_cutover_acceptance.py_test_websocket_static_launcher_shortcut_and_errors_are_safe-a7736b5b206b4e3b904e10abe27c8228"
echo LOCAL REALTIME DASHBOARD - NO LIVE TRADING
"C:\Python314\python.exe" -m binance_spot_bot.cli dashboard-v2 --host 127.0.0.1 --port 8800 --find-free-port

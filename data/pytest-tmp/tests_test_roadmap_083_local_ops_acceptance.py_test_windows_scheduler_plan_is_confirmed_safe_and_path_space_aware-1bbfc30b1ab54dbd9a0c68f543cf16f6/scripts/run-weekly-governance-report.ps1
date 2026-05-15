$ErrorActionPreference = 'Stop'
$env:LIVE_TRADING_ENABLED = 'false'
$env:KILL_SWITCH = 'true'
Set-Location -LiteralPath 'C:\Users\highlife\Desktop\Neural network binance spot\data\pytest-tmp\tests_test_roadmap_083_local_ops_acceptance.py_test_windows_scheduler_plan_is_confirmed_safe_and_path_space_aware-1bbfc30b1ab54dbd9a0c68f543cf16f6\Repo With Spaces'
python -m binance_spot_bot.cli weekly-governance-report --json

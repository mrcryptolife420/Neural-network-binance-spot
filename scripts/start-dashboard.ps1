$ErrorActionPreference = "Stop"
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $projectRoot
& (Join-Path $PSScriptRoot "check-local-env.ps1")
$env:PYTHONPATH = "src"
$env:LIVE_TRADING_ENABLED = "false"
$env:KILL_SWITCH = "true"
python -m binance_spot_bot.cli control-center --start-port 8503

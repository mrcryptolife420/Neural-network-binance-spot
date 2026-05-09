$ErrorActionPreference = "Stop"
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $projectRoot
$env:PYTHONPATH = "src"
$env:LIVE_TRADING_ENABLED = "false"
$env:KILL_SWITCH = "true"
python scripts\check-all.py @args

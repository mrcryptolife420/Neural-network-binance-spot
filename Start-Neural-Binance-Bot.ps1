$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$env:LIVE_TRADING_ENABLED = "false"
$env:KILL_SWITCH = "true"
$env:PYTHONPATH = Join-Path $PWD "src"
& (Join-Path $PSScriptRoot "scripts\start-dashboard.ps1")

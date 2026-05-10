$ErrorActionPreference = "Stop"
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $projectRoot
& (Join-Path $PSScriptRoot "check-local-env.ps1")
$env:PYTHONPATH = "src"
$env:LIVE_TRADING_ENABLED = "false"
$env:KILL_SWITCH = "true"
$result = python -m binance_spot_bot.cli control-center --start-port 8503
$result
if ($LASTEXITCODE -ne 0) {
    Write-Host "Dashboard start failed. Check data\\logs\\control-center.err.log" -ForegroundColor Red
    Read-Host "Press Enter to close"
    exit $LASTEXITCODE
}

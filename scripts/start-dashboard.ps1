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
try {
    $payload = $result | ConvertFrom-Json
    Write-Host ("Dashboard URL: " + $payload.url) -ForegroundColor Green
    Write-Host ("Launch evidence: " + $payload.evidence_path)
    Write-Host ("Logs: " + $payload.log_path)
    Write-Host ("Error logs: " + $payload.error_log_path)
    Write-Host "Live trading disabled; kill switch enabled." -ForegroundColor Yellow
}
catch {
    Write-Host "Dashboard started; JSON launch payload could not be parsed." -ForegroundColor Yellow
}

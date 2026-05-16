$ErrorActionPreference = "Stop"
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $projectRoot
& (Join-Path $PSScriptRoot "check-local-env.ps1")
$env:PYTHONPATH = Join-Path $projectRoot "src"
$env:LIVE_TRADING_ENABLED = "false"
$env:KILL_SWITCH = "true"
$python = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }
$result = & $python -m binance_spot_bot.cli control-center --start-port 8503
$result
if ($LASTEXITCODE -ne 0) {
    Write-Host "Dashboard V2 start failed. Check data\\logs\\dashboard-v2.err.log" -ForegroundColor Red
    Read-Host "Press Enter to close"
    exit $LASTEXITCODE
}
try {
    $payload = $result | ConvertFrom-Json
    Write-Host ("Dashboard V2 URL: " + $payload.url) -ForegroundColor Green
    Write-Host ("Launch evidence: " + $payload.evidence_path)
    Write-Host ("Logs: " + $payload.log_path)
    Write-Host ("Error logs: " + $payload.error_log_path)
    Write-Host "Live trading disabled; kill switch enabled." -ForegroundColor Yellow
}
catch {
    Write-Host "Dashboard started; JSON launch payload could not be parsed." -ForegroundColor Yellow
}

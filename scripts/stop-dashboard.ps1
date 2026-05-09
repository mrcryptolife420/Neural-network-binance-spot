$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$pidFile = Join-Path $projectRoot "data\logs\dashboard.pid"
if (-not (Test-Path $pidFile)) {
    Write-Host "No dashboard PID file found."
    exit 0
}

$pidValue = Get-Content $pidFile -Raw
$pidValue = $pidValue.Trim()
if (-not $pidValue) {
    Remove-Item $pidFile -Force
    exit 0
}

$proc = Get-Process -Id ([int]$pidValue) -ErrorAction SilentlyContinue
if ($proc) {
    Stop-Process -Id $proc.Id -Force
    Write-Host "Stopped dashboard process $($proc.Id)."
}
else {
    Write-Host "Dashboard process was not running."
}
Remove-Item $pidFile -Force

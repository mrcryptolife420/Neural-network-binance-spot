$ErrorActionPreference = "Stop"

Write-Host "Checking local bot environment..."
$python = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }
$pythonCommand = Get-Command $python -ErrorAction SilentlyContinue
if (-not $pythonCommand) {
    throw "Python was not found on PATH."
}

$version = & $python --version
Write-Host "Python: $version"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
if (-not (Test-Path (Join-Path $projectRoot "src\binance_spot_bot\dashboard_v2\app.py"))) {
    throw "Project files were not found under $projectRoot"
}

& $python -c "import fastapi, uvicorn" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Dashboard V2 dependencies missing. Installing local UI package..." -ForegroundColor Yellow
    & $python -m pip install -e ".[ui]"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install Dashboard V2 dependencies. Run manually: $python -m pip install -e `".[ui]`""
    }
}

Write-Host "Dashboard V2 dependencies: ok"
Write-Host "Environment check ok."

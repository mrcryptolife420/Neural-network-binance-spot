$ErrorActionPreference = "Stop"

Write-Host "Checking local bot environment..."
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    throw "Python was not found on PATH."
}

$version = & python --version
Write-Host "Python: $version"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
if (-not (Test-Path (Join-Path $projectRoot "src\binance_spot_bot\ui\streamlit_app.py"))) {
    throw "Project files were not found under $projectRoot"
}

try {
    & python -c "import streamlit, plotly" 2>$null
    Write-Host "UI dependencies: ok"
}
catch {
    throw "Missing UI dependencies. Run: pip install -e `".[ui]`""
}

Write-Host "Environment check ok."

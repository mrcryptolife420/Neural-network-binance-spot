$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $projectRoot
& (Join-Path $PSScriptRoot "check-local-env.ps1")

$env:PYTHONPATH = "src"
$env:LIVE_TRADING_ENABLED = "false"
$env:KILL_SWITCH = "true"

$logsDir = Join-Path $projectRoot "data\logs"
New-Item -ItemType Directory -Force -Path $logsDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$outLog = Join-Path $logsDir "dashboard-$stamp.out.log"
$errLog = Join-Path $logsDir "dashboard-$stamp.err.log"
$pidFile = Join-Path $logsDir "dashboard.pid"

function Test-PortFree([int]$Port) {
    $client = New-Object Net.Sockets.TcpClient
    try {
        $result = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
        $connected = $result.AsyncWaitHandle.WaitOne(200)
        if ($connected) {
            $client.EndConnect($result)
            return $false
        }
        return $true
    }
    catch {
        return $true
    }
    finally {
        $client.Close()
    }
}

$port = 8503
while (-not (Test-PortFree $port)) {
    $port += 1
}

Write-Host "Starting dashboard on http://127.0.0.1:$port"
$args = @(
    "-m", "streamlit", "run", "src/binance_spot_bot/ui/streamlit_app.py",
    "--server.port", "$port",
    "--server.headless", "true"
)
$proc = Start-Process -FilePath "python" -ArgumentList $args -WorkingDirectory $projectRoot -PassThru -WindowStyle Hidden -RedirectStandardOutput $outLog -RedirectStandardError $errLog
Set-Content -Path $pidFile -Value $proc.Id -Encoding ascii

$deadline = (Get-Date).AddSeconds(30)
do {
    Start-Sleep -Milliseconds 500
    try {
        $tcp = New-Object Net.Sockets.TcpClient("127.0.0.1", $port)
        $tcp.Close()
        Start-Process "http://127.0.0.1:$port"
        Write-Host "Dashboard opened. PID: $($proc.Id)"
        Write-Host "Live trading remains disabled."
        exit 0
    }
    catch {
    }
} while ((Get-Date) -lt $deadline)

throw "Dashboard did not become reachable. Check $errLog"

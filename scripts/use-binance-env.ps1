param(
    [ValidateSet("testnet", "demo")]
    [string]$Profile = "testnet",
    [switch]$PersistUser
)

function Read-SecretText($Prompt) {
    $secure = Read-Host $Prompt -AsSecureString
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
}

function Set-BotEnv($Name, $Value) {
    Set-Item -Path "Env:$Name" -Value $Value
    if ($PersistUser) {
        [Environment]::SetEnvironmentVariable($Name, $Value, "User")
    }
}

$apiKey = Read-SecretText "Binance $Profile API key"
$apiSecret = Read-SecretText "Binance $Profile API secret"

if ($Profile -eq "demo") {
    $baseUrl = "https://demo-api.binance.com"
}
else {
    $baseUrl = "https://testnet.binance.vision"
}

Set-BotEnv "TRADING_MODE" "testnet"
Set-BotEnv "BINANCE_API_KEY" $apiKey
Set-BotEnv "BINANCE_API_SECRET" $apiSecret
Set-BotEnv "BINANCE_TESTNET_BASE_URL" $baseUrl
Set-BotEnv "LIVE_TRADING_ENABLED" "false"
Set-BotEnv "KILL_SWITCH" "true"

Write-Host "Binance $Profile environment loaded for this PowerShell session."
Write-Host "Trading mode: testnet"
Write-Host "Base URL: $baseUrl"
Write-Host "Live trading remains disabled."
if ($PersistUser) {
    Write-Host "Values were also saved to the Windows User environment."
}

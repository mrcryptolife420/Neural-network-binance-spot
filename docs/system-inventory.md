# System Inventory

The system inventory scans local repository files and maps subsystems to modules, CLI commands, tests, docs, evidence artifacts, and roadmap numbers.

It is read-only, offline, secret-redacted, and always reports `live_trading_enabled=false`.

Run:

```powershell
python -m binance_spot_bot.cli system-inventory --json
```

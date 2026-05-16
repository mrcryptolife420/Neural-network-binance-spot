# Split Governance

Split governance enforces chronological train, validation, and test separation for demo-derived datasets.

Rules:

- test data is not used for tuning
- leakage reports must pass
- duplicate or too-small datasets block validation
- split reports keep `live_trading_enabled=false`

Use:

```powershell
python -m binance_spot_bot.cli split-governance-check --json
```

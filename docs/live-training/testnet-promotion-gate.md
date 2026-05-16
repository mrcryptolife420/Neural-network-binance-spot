# Testnet Promotion Gate

The testnet promotion gate blocks until demo session targets, dataset quality, model validation, and paper replay are ready.

Promotion state `ready_for_testnet_rehearsal` allows a controlled testnet rehearsal only. It does not enable live trading.

Use:

```powershell
python -m binance_spot_bot.cli testnet-promotion-check --json
```

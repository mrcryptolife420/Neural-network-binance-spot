# Testnet Rehearsal Runner

The testnet rehearsal runner verifies a controlled testnet-only order lifecycle rehearsal.

Safety requirements:

- explicit `RUN_TESTNET_REHEARSAL_ONLY` confirmation
- testnet base URL only
- promotion gate must pass
- live trading remains disabled

Use:

```powershell
python -m binance_spot_bot.cli testnet-rehearsal-run --confirm RUN_TESTNET_REHEARSAL_ONLY --json
```

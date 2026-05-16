# Demo Spot Recording Hardening

Demo spot recording stores local session manifests with event counts, event hashes, profile id, session id, symbols, timestamps, and no-live flags.

The recorder output feeds the demo dataset vault. It is intentionally local and does not enable live orders.

Use:

```powershell
python -m binance_spot_bot.cli demo-recordings-verify --json
```

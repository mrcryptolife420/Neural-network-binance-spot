# Demo Dataset Vault

The demo dataset vault normalizes recorder sessions and stores dataset manifests under `data/live-training/demo-vault/`.

Vault responsibilities:

- ingest recorder sessions
- preserve normalized events
- reject or block unsafe secret-like content
- produce a manifest hash
- keep `live_trading_enabled=false`

Use:

```powershell
python -m binance_spot_bot.cli demo-vault-ingest --json
```

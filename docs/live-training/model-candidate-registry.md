# Model Candidate Registry

The registry tracks model candidates, dataset versions, strategy ids, validation paths, replay status, testnet rehearsal status, and promotion state.

Promotion cannot skip required states. A candidate must pass dataset, validation, paper replay, and testnet gates before it can become a live-readiness review candidate.

Use:

```powershell
python -m binance_spot_bot.cli model-candidates --json
```

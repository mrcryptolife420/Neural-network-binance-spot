# Demo Session Targets

The target plan defines the minimum demo spot evidence required before testnet rehearsal.

Required coverage includes session count, runtime, candles, signals, risk allow/block decisions, order previews, test orders, demo orders, fills, rejected or cancelled cases, spread samples, latency samples, reconciliation runs, and market regimes.

Market regimes:

- calm
- volatile
- low volume
- high spread
- trending
- ranging

Use:

```powershell
python -m binance_spot_bot.cli demo-session-targets --json
python -m binance_spot_bot.cli demo-session-progress --json
```

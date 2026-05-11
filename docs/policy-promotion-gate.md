# Policy Promotion Gate

Roadmap 082 promotion is paper-only. A policy can become champion only when the operator confirms the action and the gate sees evidence for benchmark pass, robustness pass, overfit guard, paper approval, and no signed or live endpoint usage.

Required evidence fields:

- `benchmark_status`: `pass`, `ok`, or `true`
- `robustness_score`: at or above the configured threshold
- `overfit_guard`: `pass`, `ok`, or `true`
- `paper_approval`: `approved`, `pass`, or `true`
- `live_trading_enabled`: `false`
- `signed_endpoint_used`: `false`

The gate rejects live-like policy statuses and returns explicit blocker reasons. It does not call Binance and does not read API keys.

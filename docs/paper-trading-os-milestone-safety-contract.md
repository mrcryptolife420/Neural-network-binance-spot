# Paper Trading OS Milestone Safety Contract

Roadmap 100 is paper-only. It must not enable live trading, add live mode, execute signed real-order endpoints, or require Binance account endpoints.

Required invariants:

- Dashboard/runtime modes stay limited to demo, paper, and testnet-readiness.
- Milestone profiles force `LIVE_TRADING_ENABLED=false` and `KILL_SWITCH=true`.
- Demo execution remains explicitly armed and confirm-gated.
- Production readiness means simulation readiness, not live deployment.
- Audit reports and bundles include no-live proof and remain secret-free.
- Operator sign-off is local, audit-only, and paper-ops scoped.

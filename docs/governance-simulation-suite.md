# Governance Simulation Suite

The governance simulation suite exercises paper-only cases without Binance API calls.

Covered cases:

- `challenger_beats`
- `challenger_fails`
- `too_few_samples`
- `drawdown_breach`
- `data_quality_warning`
- `policy_violation`
- `operator_not_confirmed`

Each simulation returns rollout plan, experiment report, stopping result, governance decision, and `live_trading_enabled: false`.

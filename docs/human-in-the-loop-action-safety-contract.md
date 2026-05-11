# Human-in-the-Loop Action Safety Contract

The Action Center is local-only and paper/demo operations only.

- AI/Ops may create proposals, but never executes actions.
- Every action is validated, journaled, and requires an operator decision.
- Forbidden actions include live trading, signed orders, account endpoints, withdrawals, secrets reveal, and arbitrary shell.
- Confirm-required actions need an exact confirm phrase.
- Execution uses the Roadmap 083 local command allowlist with `LIVE_TRADING_ENABLED=false` and `KILL_SWITCH=true`.
- Outputs, reports, journals, and bundles are redacted.


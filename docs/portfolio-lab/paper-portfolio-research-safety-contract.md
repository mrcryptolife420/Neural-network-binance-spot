# Portfolio Lab Safety Contract

Portfolio Lab is local paper research only.

- `LIVE_TRADING_ENABLED=false` is required.
- `KILL_SWITCH=true` is expected during validation.
- API keys are not required.
- Signed, account and order endpoints are out of scope.
- Portfolio baskets are research inputs, not account allocations.
- Allocation proposals are paper research candidates.
- Reports must include `live_trading_enabled=false`.
- Reports must include the no-live, no-advice and paper-only statements.
- Evidence bundles must redact secret-like values.

Required confirmation for a simulation run:

```text
RUN_PAPER_PORTFOLIO_RESEARCH_ONLY
```


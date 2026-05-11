# Paper Experiment Split

The split manager assigns paper observations to champion or challenger without touching Binance account or order endpoints.

Supported splits:

- `allocation`: deterministic hash bucket by symbol and seed
- `symbol`: symbol-level deterministic assignment
- `time_slice`: assignment per symbol and time bucket
- `canary`: explicit challenger symbols, all other symbols remain champion

Allocation must be non-negative and total 100 percent. The split output records guardrails for paper-only mode and deterministic seed.

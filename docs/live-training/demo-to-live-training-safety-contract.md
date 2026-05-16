# Demo-to-Live Training Safety Contract

Live trading remains disabled in this training workflow.

Rules:

- Only local, public, demo, paper, or testnet evidence is allowed.
- The dataset builder must not call live account or live order endpoints.
- Raw API keys, secrets, tokens, and secret-like values must not be written to datasets, logs, reports, or evidence bundles.
- Testnet rehearsal requires explicit operator confirmation.
- Live execution still requires a separate implementation and approval gate.
- Reports are research evidence only, not financial advice or profit claims.

Acceptance evidence:

- `demo-session-progress` reports `live_trading_enabled=false`.
- `testnet-rehearsal-run` blocks without `RUN_TESTNET_REHEARSAL_ONLY`.
- `live-candidate-check` keeps `live_execution_enabled=false`.

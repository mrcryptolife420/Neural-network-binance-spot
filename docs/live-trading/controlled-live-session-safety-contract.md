# Controlled Live Session Safety Contract

Controlled live sessions are disabled by default and never start from the launcher or normal dashboard start flow.

Rules:

- Every session requires Roadmap 117 and Roadmap 118 evidence references.
- Every session has max orders, quote exposure, single-order quote, loss, duration, spread, data-age, and open-order budgets.
- Every order requires preview hash, arm token, healthy heartbeat, budget allow, and no disarm trigger.
- A next order is blocked until reconciliation passes.
- Restart, profile/config/key change, kill switch, stale data, spread breach, connectivity loss, reconciliation mismatch, unknown order state, unexpected open order, max orders, max loss, and evidence-writer failure disarm the session.
- Evidence must be redacted and local.
- This is operational evidence, not financial advice.

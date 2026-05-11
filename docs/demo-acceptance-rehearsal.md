# Demo Acceptance Rehearsal

Demo Acceptance Rehearsal bundles the existing local readiness checks into one operator run.

Run from CLI:

```powershell
spot-bot demo-acceptance-rehearsal --json
spot-bot demo-acceptance-rehearsal --browser-url http://127.0.0.1:8503 --json
spot-bot demo-acceptance-rehearsal --strict
```

Run from dashboard:

1. Open Readiness.
2. Use `Run rehearsal`.
3. Review latest steps, blockers, warnings, recent rehearsals and trend rows.

The rehearsal runs config validation, preflight, launch evidence, dashboard smoke, optional browser smoke, check-all, pilot double-start idempotency smoke, operator diagnostics, Demo Execution Drill preview, optional test-order-only, operator evidence and evidence scorecard.

Artifacts are written under:

```text
data/evidence/rehearsals/
```

Pilot start idempotency evidence is written to:

```text
data/evidence/pilot-start-idempotency.json
```

Operator diagnostics evidence is written to:

```text
data/evidence/diagnostics/latest-diagnostics.json
```

`--strict` exits non-zero unless the final status is `pass`. This is not live-trading approval. Live trading remains disabled.

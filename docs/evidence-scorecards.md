# Evidence Scorecards

Evidence scorecards summarize whether the local demo/paper operator evidence is good enough to continue.

Generate a scorecard:

```powershell
spot-bot evidence-scorecard --json
spot-bot evidence-scorecard --strict
```

The latest report is written to:

```text
data/evidence/scorecards/latest-scorecard.json
```

## Status

- `pass`: no blockers and no warnings.
- `warn`: no blockers, but evidence is missing or incomplete.
- `fail`: one or more safety blockers were found.

## Inputs

- dashboard launch evidence;
- dashboard browser smoke;
- operator evidence;
- Demo Execution Drill evidence;
- pilot start idempotency evidence;
- operator diagnostics evidence;
- runner health;
- optional check-all artifact.

This is not live-trading approval. Live trading remains disabled.

Demo Acceptance Rehearsal automatically generates a scorecard as one step in the bundled operator run:

```powershell
spot-bot demo-acceptance-rehearsal --json
```

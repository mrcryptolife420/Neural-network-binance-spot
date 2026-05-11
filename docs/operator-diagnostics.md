# Operator Diagnostics

Operator diagnostics summarizes local bot health for demo/paper operations. Live trading remains disabled.

Run from CLI:

```powershell
spot-bot diagnostics --json
spot-bot diagnostics --strict
```

Run from dashboard:

1. Open Readiness.
2. Use `Recovery & Diagnostics`.
3. Review blockers, warnings, recommended actions and artifact inventory.

Status meanings:

- `ok`: no blockers or warnings.
- `warn`: missing, stale or invalid local evidence needs refresh.
- `fail`: a blocking local safety condition exists.

Diagnostics checks artifact freshness, pilot-run state, runner lock state, package availability and live trading safety. It never approves live trading.

Diagnostics reports append trend rows to `data/evidence/diagnostics/history.jsonl` when written by rehearsal or report workflows.

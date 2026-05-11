# Demo Pilot State Recovery

Live trading remains disabled. This flow only applies to the local Demo Spot pilot.

Pilot lifecycle states:

- `ready`: start gate passed and the run can move to `running`.
- `running`: a pilot run is active. Pressing start again is idempotent and keeps the same run.
- `stopping`: safe stop is in progress. Wait until it reaches `completed` or `resume_required`.
- `resume_required`: open orders, reconciliation issues or an interrupted run need operator action.
- `completed`: stop flow finished cleanly.
- `failed`: the run ended with a blocking failure.

If the dashboard shows `Pilot is already running`, do not press start repeatedly. Use `Safe stop pilot` when you want to end the active run. If the state is `resume_required`, reconcile or cancel Demo Spot orders, then use `Mark resolved`.

The dashboard start button is disabled when runtime or pilot state makes a new start unsafe. The start flow records an idempotent checkpoint instead of creating a second run when an existing run is already `running`.

Demo Acceptance Rehearsal writes `data/evidence/pilot-start-idempotency.json` to prove a double start keeps the same run id and never transitions `running -> ready`.

# Operator Workflow

Status: local paper/testnet-readiness only. Live trading remains disabled.

1. Start the dashboard with `Start Bot Dashboard.cmd`.
2. Confirm the header shows `Live: disabled`, `Kill switch: on`, active mode, profile, source, base URL and runner state.
3. Inspect `data/checks/dashboard/launch-evidence.json` if the launcher does not open the browser.
4. Run Local Demo first.
5. Use Demo Spot Trading only for local paper/demo fills.
6. Use Demo Execution Drill to preview, test-order-only, then explicitly confirm any Demo Spot order.
7. Use Demo Pilot to connect, reconcile, arm/disarm, start/stop runner and export reports. If the pilot is already `running`, use `Safe stop pilot`; if it is `resume_required`, reconcile/cancel and use `Mark resolved`.
8. Run `spot-bot dashboard-browser-smoke --url <dashboard-url> --seconds 15` for a visual smoke.
9. Use `Export operator evidence` in the dashboard or `spot-bot dashboard-operator-evidence`.
10. Generate an Evidence Scorecard from Readiness or `spot-bot evidence-scorecard --json`.
11. Run Demo Acceptance Rehearsal from Readiness or `spot-bot demo-acceptance-rehearsal --json`.
12. Open `Recovery & Diagnostics` in Readiness or run `spot-bot diagnostics --json` when anything looks stuck.
13. Export a support bundle with `spot-bot support-bundle --json` before large changes.
14. Open Sessions to replay or compare runs.
15. Open Readiness to see evidence blockers and next safe steps.

No step requires real API keys. Binance Demo/Testnet keys are optional readiness inputs and must stay session-only unless a later secure storage flow is explicitly used.

See `docs/demo-pilot-state-recovery.md`, `docs/operator-diagnostics.md` and `docs/support-bundle.md` for recovery actions.

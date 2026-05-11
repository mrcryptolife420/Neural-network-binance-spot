# Operator Local Ops

Local operator ops adds diagnostics trends, retention previews, incident timelines and operator reports. Live trading remains disabled.

Useful commands:

```powershell
spot-bot retention-preview --json
spot-bot state-archive --json
spot-bot support-bundle-verify --bundle data/support/support-bundle.zip --json
spot-bot incident-timeline --json
spot-bot incident-timeline --markdown --json
spot-bot operator-report --json
spot-bot operator-report-diff --json
spot-bot operator-quality-gate --json
spot-bot operator-health-score --json
spot-bot artifact-catalog --json
spot-bot artifact-catalog --category checks --suffix .json --stale-days 7 --json
spot-bot diagnostics-baseline --write --json
spot-bot report-index --json
spot-bot support-bundles-verify --json
spot-bot support-bundle-restore-preview --bundle data/support/support-bundle.zip --json
spot-bot redaction-self-test --json
spot-bot local-ops-snapshot --json
spot-bot operator-command-manifest --json
spot-bot evidence-manifest --json
spot-bot evidence-chain --json
spot-bot environment-doctor --json
spot-bot data-growth-budget --budget-bytes 100000000 --json
spot-bot rehearsal-profiles --json
```

Retention archive is preview-only and does not delete evidence. Operator reports are written under `data/reports/operator/`.

The local ops snapshot combines diagnostics, a health score with next best action, baseline drift, artifact catalog filters and staleness groups, rehearsal profiles, retention preview, timeline, report index and diff, support bundle verification, environment doctor checks, data growth budget, redaction self-test and the safe operator command manifest. Live trading remains disabled.

Restore preview is deliberately non-destructive: it reads the bundle manifest and summarizes files without extracting or overwriting local state.

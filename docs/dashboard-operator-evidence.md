# Dashboard Operator Evidence

Roadmap 025 adds local evidence for the Windows one-click dashboard flow.

## Artifacts

- `data/checks/dashboard/launch-evidence.json`: created by `spot-bot control-center`.
- `data/checks/dashboard/browser-smoke.json`: created by `spot-bot dashboard-browser-smoke`.
- `data/checks/dashboard/screenshots/`: Playwright screenshots when browser automation is available.
- `data/evidence/dashboard/operator-evidence-*.json`: operator export from CLI or dashboard button.
- `data/evidence/demo-execution/demo_execution_drill.json`: latest Demo Execution Drill evidence.
- `data/evidence/scorecards/latest-scorecard.json`: latest quality gate scorecard.

## Commands

```powershell
Start Bot Dashboard.cmd
spot-bot dashboard-browser-smoke --url http://127.0.0.1:8503 --seconds 15
spot-bot dashboard-operator-evidence --mode demo --profile local-demo --source demo
spot-bot demo-execution-report
spot-bot evidence-scorecard --json
```

## Safety Contract

Every evidence payload must include:

- `live_trading_enabled: false`
- `kill_switch: true` where launch/operator evidence applies
- no raw API keys, API secrets, signatures or listen keys

The evidence proves local operator readiness only. It is not a live-trading approval gate.

# Dashboard Smoke Tests

Run the static dashboard smoke command:

```powershell
spot-bot dashboard-smoke --seconds 10
```

Expected result:

- JSON status is `ok`.
- `live_trading_enabled` is `false`.
- Chart keys are unique.
- The smoke artifact is written under the configured data directory.

For an end-to-end local visual check:

```powershell
Start Bot Dashboard.cmd
spot-bot dashboard-browser-smoke --url http://127.0.0.1:8503 --seconds 15
spot-bot dashboard-operator-evidence --mode demo --profile local-demo --source demo
spot-bot demo-acceptance-rehearsal --browser-url http://127.0.0.1:8503 --json
```

Expected browser smoke result:

- JSON status is `ok`.
- `live_trading_enabled` is `false`.
- No Streamlit exception marker is visible.
- Screenshot paths are written when Playwright is available.

Then run:

```powershell
pytest tests/test_roadmap_023_dashboard_stability.py tests/test_roadmap_024_dashboard_architecture.py tests/test_roadmap_025_dashboard_browser_smoke.py tests/test_roadmap_025_operator_evidence.py
```

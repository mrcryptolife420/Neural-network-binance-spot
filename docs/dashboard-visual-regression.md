# Dashboard Visual Regression

Current coverage has two layers:

- `spot-bot dashboard-smoke` validates the static dashboard contract.
- `spot-bot dashboard-browser-smoke --url http://127.0.0.1:8503 --seconds 15` validates a running local dashboard.

The browser smoke checks the title, live-disabled marker, critical tabs, and known Streamlit exception markers. When Playwright is installed, it captures screenshots for Overview, Demo Spot Trading, Demo Pilot, and Logs & Security under `data/checks/dashboard/screenshots/`.

Use `--update-baseline` only for local operator baselines. Baseline images stay in `data/` and are not committed by default.

# Dashboard Performance Budgets

Local operator budget:

- Dashboard import path should stay lightweight and avoid network calls during import.
- Smoke checks should complete in under 10 seconds on Windows 11.
- Runner telemetry charts should render from persisted rows without blocking the runner loop.
- New expensive diagnostics should be behind a button or explicit refresh action.

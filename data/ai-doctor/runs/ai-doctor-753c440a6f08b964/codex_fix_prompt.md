# Codex Fix Prompt

Read the AI Doctor bundle first, then inspect the suspect files.

Safety constraints:
- do not start live trading.
- Do not place or cancel orders.
- Do not expose secrets.
- Keep LIVE_TRADING_ENABLED=false and KILL_SWITCH=true in tests.

Suspect files:
- src/binance_spot_bot/cli.py
- src/binance_spot_bot/dashboard_v2/app.py

Acceptance tests:
- `python -m compileall -q src tests`
- `pytest -q`
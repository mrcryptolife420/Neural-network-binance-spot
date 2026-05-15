# Dashboard V2 Cutover Safety Contract

Dashboard V2 is a local operator UI for demo, paper and testnet-readiness workflows only.

- Default bind address is `127.0.0.1`.
- Supported modes are `demo`, `paper` and `testnet-readiness`.
- Live trading mode, signed order endpoints and real account workflows are outside this cutover.
- Streamlit remains available as a fallback until the cutover readiness gate passes.
- Static frontend assets must not require external CDN, remote fonts or remote telemetry.
- Error reports, support diagnostics and evidence bundles must redact secret-like values.
- Every report must include `LOCAL REALTIME DASHBOARD - NO LIVE TRADING`.
- Rollback means launching the Streamlit legacy dashboard with `python -m binance_spot_bot.cli dashboard --legacy-streamlit`.

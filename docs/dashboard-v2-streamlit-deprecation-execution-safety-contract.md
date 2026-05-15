# Streamlit Deprecation Execution Safety Contract

Deprecation is local-only and does not remove Streamlit in Roadmap 108.

- Dashboard V2 remains limited to `demo`, `paper` and `testnet-readiness`.
- V2-only operator mode must not import Streamlit.
- Streamlit fallback stays reachable with `python -m binance_spot_bot.cli dashboard --legacy-streamlit`.
- No live mode, signed order route, real account workflow or remote telemetry is introduced.
- No-live proof, browser smoke, support/evidence export and fallback drill are required before any later removal candidate.

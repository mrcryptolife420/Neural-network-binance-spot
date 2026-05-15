# Dashboard V2 Safety Contract

Dashboard V2 is local-only and paper/demo/testnet-readiness only.

Rules:

- Supported modes are `demo`, `paper`, and `testnet-readiness`.
- Live mode, live routes, signed real-order endpoints, and account workflows are forbidden.
- Every root payload includes `live_trading_enabled=false`.
- WebSocket events and API responses are redacted.
- The frontend always shows `LOCAL REALTIME DASHBOARD - NO LIVE TRADING`.
- Streamlit remains a fallback and is not removed in Roadmap 104.

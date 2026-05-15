# Dashboard V2 Parity Safety Contract

Dashboard V2 parity work is local-only.

Rules:

- No live mode in routes, selectors, API payloads, tests, or docs.
- All POST actions use Dashboard V2 action policy.
- Streamlit remains a legacy fallback and receives no extra capabilities.
- Credential panels expose status or fingerprints only.
- Page parity cannot introduce live pages.
- Root payloads include `live_trading_enabled=false`.

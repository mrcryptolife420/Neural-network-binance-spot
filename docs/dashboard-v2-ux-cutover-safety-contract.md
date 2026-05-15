# Dashboard V2 UX Cutover Safety Contract

Dashboard V2 UX changes are local-only and limited to `demo`, `paper` and `testnet-readiness`.

- No live mode appears in navigation, forms, action cards, CLI commands or docs.
- No guided action may bypass backend safety policy.
- No-live proof remains visible in the V2-first layout.
- Streamlit remains a fallback until a later deprecation gate explicitly changes that policy.
- UX feedback, metrics and evidence are local-only and redacted.

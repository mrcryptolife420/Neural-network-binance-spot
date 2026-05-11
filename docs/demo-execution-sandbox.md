# Demo Execution Sandbox

The Demo Execution Sandbox is the operator-controlled bridge between local paper/demo behavior and Binance Demo Spot order APIs.

## Modes

- Preview: builds a quantized order request from symbol, side, quote size and filters. No credentials or network calls are required.
- Test order only: calls `/api/v3/order/test` when Demo Spot credentials and profile are present. It never calls `place_order`.
- Place demo order: calls test order first, then Demo Spot `place_order` only when explicit confirmation, Demo Spot profile, demo base URL, credentials, armed state and gates pass.
- Query/cancel: uses signed Demo Spot order endpoints and requires confirmation for cancel.

## Safety

- Live trading is blocked in this sandbox.
- Evidence is redacted before writing.
- Raw API keys and secrets must never appear in logs or reports.
- Default operator path is preview first, test order second, place order last.

## Artifacts

Sandbox evidence is written to:

```text
data/evidence/demo-execution/demo_execution_drill.json
data/evidence/demo-execution/demo_execution_drill_<timestamp>.json
```

Each payload includes `live_trading_enabled: false`.

# Paper OS Stabilization Safety Contract

Roadmap 101 is paper-only stabilization. It may classify, prioritize, report, and verify blockers, but it must not add live mode, signed real-order endpoints, account workflows, or API-key requirements.

Rules:

- No-live proof failures are P0 and cannot be waived.
- Secret-like evidence is P0 and blocks the gate.
- Waivers require reason, owner, expiry, and evidence scope.
- Flaky checks remain visible in reports.
- Slow checks may be optimized but safety checks cannot be skipped for speed.
- All stabilization reports include `live_trading_enabled=false`.

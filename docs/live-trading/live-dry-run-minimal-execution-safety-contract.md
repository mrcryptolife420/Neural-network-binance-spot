# Live Dry-Run Minimal Execution Safety Contract

Live trading remains locked by default.

Rules:

- The one-click launcher must never start live order placement.
- The normal dashboard start flow must never place live orders.
- Live dry-run, read-only account verification, order preview, sizing guard, kill-switch drill, and manual confirmation are required before any first-order gate.
- First-order execution is limited to an explicit, one-time, tiny capped gate.
- Emergency stop must always be available.
- Evidence must be secret-free and must state whether execution was dry-run only.
- Output is operational evidence, not financial advice.

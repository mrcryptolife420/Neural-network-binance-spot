# Live Execution Adapter

The live execution adapter is only reachable through the first-order gate. Normal runtime, launcher, demo, paper, and testnet flows do not call this path.

Tests use a fake adapter that records exactly one place-order call and blocks the second call.

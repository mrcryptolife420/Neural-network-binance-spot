# Runtime State Model

Roadmap: 095

`runtime_state.py` defines explicit runtime state dataclasses:
- identity
- lifecycle
- market
- paper
- model
- demo
- reports
- safety

The model is intentionally separate from `BotRuntime` so refactors can move one concern at a time while preserving the existing dashboard snapshot contract.

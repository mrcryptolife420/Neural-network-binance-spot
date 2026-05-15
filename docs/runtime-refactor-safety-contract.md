# Runtime Refactor Safety Contract

Roadmap: 095

Runtime decomposition must keep the trading boundary unchanged. Event buses, snapshot builders and batch writers are observability and local-artifact tools only.

Rules:
- No new live mode.
- No event handler may place orders automatically.
- Snapshot payloads are redacted before export.
- Snapshot profiles must enforce payload limits.
- Session batch writes are local JSONL artifacts only.
- Demo-pilot counters are isolated from execution decisions.
- Existing `BotRuntime` public API remains backward compatible.

Validation:
- Runtime event bus publishes and drains events without execution side effects.
- Snapshot profiles redact secret-like payloads and limit list/dict size.
- Step pipeline emits stage events and stops on failed stage.
- Batch writer writes redacted JSONL and never enables live trading.

# Runtime Event Bus

Roadmap: 095

`RuntimeEventBus` accepts typed `RuntimeEvent` objects and legacy dictionaries.

Guarantees:
- publishing an event only stores/notifies local handlers;
- events are redacted on dictionary export;
- `drain()` remains backward compatible for old tests;
- `drain_dicts()` is available for artifact writers.

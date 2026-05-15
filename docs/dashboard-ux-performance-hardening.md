# Dashboard UX Performance Hardening

Roadmap: 094

Dashboard hardening covers page registry validation, stable component helpers, dashboard smoke v2, UX evidence, and expanded local dashboard surfaces without enabling live trading.

Implemented controls:

- `dashboard_smoke_v2()` checks stable chart keys, lazy page metadata, payload limits and no-live mode.
- `render_table()` caps large tables and shows truncation copy.
- `render_debug()` redacts and caps JSON payloads before display.
- Page registry metadata stores smoke-required pages and page-level render budgets.
- Dedicated lazy module boundaries exist for overview, demo spot trading, demo pilot and performance pages.

Operator impact:

- The dashboard keeps the same visual workflow.
- Large diagnostics no longer flood the UI.
- Future dashboard extraction can move one page at a time without rewriting runtime logic.

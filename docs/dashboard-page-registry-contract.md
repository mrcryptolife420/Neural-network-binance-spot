# Dashboard Page Registry Contract

Roadmap: 094

`src/binance_spot_bot/ui/page_registry.py` is the canonical dashboard page inventory.

Required fields:
- `key`: stable machine key.
- `title`: displayed tab title.
- `module`: lazy module target.
- `smoke_required`: true for operator-critical pages.
- `performance_budget_ms`: local render budget.
- `live_trading_enabled`: always false.

Critical smoke pages:
- overview
- demo_spot_trading
- demo_pilot
- performance

The registry intentionally does not execute trading logic. Page modules expose a `render_page` boundary and can delegate to existing controller code until a page is safely extracted.

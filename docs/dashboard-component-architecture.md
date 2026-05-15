# Dashboard Component Architecture

The Streamlit app stays thin by using shared UI helpers:

- `render_badges` for metric rows.
- `render_table` for tabular operator evidence.
- `render_debug` for JSON diagnostics.
- `render_plotly_chart` for all Plotly output with stable keys.

New UI work should extend these helpers or add a small focused helper before duplicating chart/table rendering logic.

Roadmap 094 adds page metadata in `ui/page_registry.py`:

- each page has a lazy module target;
- critical pages have smoke coverage flags;
- each page has a render performance budget;
- registry validation blocks live-enabled pages and invalid budgets.

Current dedicated page-module stubs delegate rendering to the existing Streamlit controller. This avoids duplicating runtime or trading logic while giving future refactors stable module boundaries.

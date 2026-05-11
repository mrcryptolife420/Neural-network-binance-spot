# Dashboard Component Architecture

The Streamlit app stays thin by using shared UI helpers:

- `render_badges` for metric rows.
- `render_table` for tabular operator evidence.
- `render_debug` for JSON diagnostics.
- `render_plotly_chart` for all Plotly output with stable keys.

New UI work should extend these helpers or add a small focused helper before duplicating chart/table rendering logic.

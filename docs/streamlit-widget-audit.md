# Streamlit Widget Audit

Current audited chart surfaces:

- Overview candlestick chart: keyed through `OVERVIEW_CANDLESTICK`.
- Overview equity chart: keyed through `OVERVIEW_EQUITY`.
- Demo Pilot runner heartbeat, counters, equity/PnL, and command status charts: keyed through the chart registry.

Regression coverage:

- `tests/test_roadmap_023_dashboard_stability.py` fails if direct unkeyed `st.plotly_chart` calls return to the UI code.
- `tests/test_roadmap_024_dashboard_architecture.py` validates page registry uniqueness and live-disabled page contracts.

Operator rule: when a new chart is added, add a registry key and a test expectation in the same change.

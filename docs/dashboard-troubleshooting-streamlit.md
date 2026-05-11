# Streamlit Troubleshooting

## Duplicate Element ID

Cause: multiple charts or widgets have identical generated Streamlit IDs.

Fix:

1. Route Plotly charts through `render_plotly_chart`.
2. Add a stable key to `chart_registry.py`.
3. Run `pytest tests/test_roadmap_023_dashboard_stability.py`.

## Blank Dashboard

Run:

```powershell
spot-bot dashboard-smoke --seconds 10
spot-bot check-all --json
```

If the smoke payload is created but Streamlit is blank, inspect the terminal that launched Streamlit for import or dependency errors.

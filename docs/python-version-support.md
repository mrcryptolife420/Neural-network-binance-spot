# Python Version Support

This project targets Python 3.12 or newer, matching `pyproject.toml`.

Supported local workflow:

```powershell
python --version
python -m pytest tests/test_roadmap_023_dashboard_stability.py tests/test_roadmap_024_dashboard_architecture.py
```

If Streamlit or Plotly fails to import, install the UI extra in the active environment before launching the dashboard.

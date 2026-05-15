# Dashboard Payload Limits

Roadmap: 094

Dashboard payload controls:
- Tables default to 250 rows.
- Debug JSON defaults to 12000 characters.
- Debug payloads pass through the existing redaction layer before display.
- Truncated payloads keep metadata showing original size and max size.

These limits are UX and safety guardrails. They prevent accidental secret exposure and keep heavy diagnostics from freezing the local Streamlit dashboard.

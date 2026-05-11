# Streamlit Widget Key Convention

All dashboard charts and high-risk controls must use stable, human-readable keys.

- Plotly charts render through `binance_spot_bot.ui.components.render_plotly_chart`.
- Chart keys live in `binance_spot_bot.ui.chart_registry`.
- Page keys live in `binance_spot_bot.ui.page_registry`.
- Keys use the pattern `<page>.<area>.<purpose>`, for example `demo_pilot.runner.heartbeat`.
- Do not let Streamlit generate chart IDs automatically; duplicate chart structures can collide.
- Live trading controls remain unavailable in the local dashboard.

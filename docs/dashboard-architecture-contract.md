# Dashboard Architecture Contract

The dashboard is a local operator control center for demo/paper operation. It must not expose live trading.

Required boundaries:

- Page order and titles are owned by `binance_spot_bot.ui.page_registry`.
- Shared Streamlit components live in `binance_spot_bot.ui.components`.
- Plotly chart IDs live in `binance_spot_bot.ui.chart_registry`.
- Page modules under `binance_spot_bot.ui.pages` define page identity and validate live-disabled context.
- Execution remains behind runtime, risk, pilot runner, and demo trading services.

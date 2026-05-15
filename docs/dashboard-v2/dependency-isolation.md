# Dependency Isolation

Run `python -m binance_spot_bot.cli dashboard-v2-dependency-isolation --json`.

Dashboard V2 must import without Streamlit. Streamlit dependencies are isolated behind `legacy-streamlit`/legacy UI extras.

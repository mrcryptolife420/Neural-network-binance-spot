# WebSocket Stability

Dashboard V2 events use local-only heartbeat, event ids, duplicate suppression and a max event size guard.

Run `python -m binance_spot_bot.cli dashboard-v2-ws-stability-smoke --json` to verify reconnect, replay, duplicate handling and backpressure reporting.

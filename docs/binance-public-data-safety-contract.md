# Binance Public Data Safety Contract

Status: active.

This project may fetch Binance Spot public market data without API keys.

Allowed public endpoints:

- `/api/v3/exchangeInfo`
- `/api/v3/klines`
- `/api/v3/uiKlines`
- `/api/v3/depth`
- `/api/v3/ticker/24hr`
- `/api/v3/ticker`
- `/api/v3/avgPrice`
- `/api/v3/trades`
- `/api/v3/aggTrades`
- `/api/v3/ticker/bookTicker`

Allowed optional public WebSocket streams:

- kline
- miniTicker
- bookTicker
- depth
- aggTrade

Forbidden for public data ingestion:

- `/api/v3/account`
- `/api/v3/order`
- `/api/v3/openOrders`
- signed `queryOrder`
- user-data actions
- withdrawals
- margin, futures or leverage endpoints

Rules:

- Public data ingestion must work without API keys.
- Public data ingestion must never set `signed=True`.
- Live trading remains disabled.
- Evidence and cache manifests must be redacted and contain `live_trading_enabled=false`.

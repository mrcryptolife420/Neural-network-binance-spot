# Public Endpoint Policy

The Market Intelligence layer only allows Binance Spot public market data methods:

- `get_exchange_info`
- `get_klines`
- `get_ui_klines`
- `get_order_book`
- `get_24hr_ticker`
- `get_rolling_ticker`
- `get_avg_price`
- `get_recent_trades`
- `get_agg_trades`
- `get_book_ticker`

Forbidden methods include account state, order creation, order cancellation, order query, open orders, test orders, and listen-key lifecycle calls.

CLI:

```powershell
python -m binance_spot_bot.cli market-intelligence-policy --json
```

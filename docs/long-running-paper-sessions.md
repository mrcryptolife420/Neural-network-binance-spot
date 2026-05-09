# Long-running paper sessions

Use `paper-session` for a bounded local paper run:

```powershell
$env:PYTHONPATH="src"
python -m binance_spot_bot.cli paper-session --symbol BTCUSDT --minutes 60 --max-steps 500 --max-paper-orders 25 --source demo
```

The command enforces budgets for time, steps, paper orders and critical alerts. It records:

- `snapshots.jsonl`
- `heartbeats.jsonl`
- `alerts.jsonl`
- `orders.jsonl`
- `fills.jsonl`
- `report/summary.md`
- `report/summary.json`
- `report/fills.csv`
- `report/equity.csv`

Use `--source demo` first. Public Binance data can be tested later with paper mode, but signed order endpoints are not used.

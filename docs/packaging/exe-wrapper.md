# EXE Wrapper

The optional Windows EXE is a thin safe wrapper around:

```powershell
python -m binance_spot_bot.cli dashboard-v2
```

It must force `LIVE_TRADING_ENABLED=false` and `KILL_SWITCH=true` and must not contain secrets.

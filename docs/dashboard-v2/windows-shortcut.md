# Windows Shortcut

Run `python -m binance_spot_bot.cli dashboard-v2-create-shortcut --json`.

The generated `.cmd` launcher sets `LIVE_TRADING_ENABLED=false`, sets `KILL_SWITCH=true`, uses localhost and starts Dashboard V2 with a free local port. No administrator rights are required.

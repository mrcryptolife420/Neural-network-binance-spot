def model_performance(pnl: float, drawdown: float): return {"status": "ok" if pnl >= 0 and drawdown <= 25 else "warn", "pnl": pnl, "drawdown": drawdown, "live_trading_enabled": False}

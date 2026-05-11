def paper_simulation_stabilizer(status: str): return {"status": "ok" if status in {"ok", "ready"} else "warn", "live_trading_enabled": False}

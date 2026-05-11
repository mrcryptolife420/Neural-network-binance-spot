def permission_drift(expected: dict, actual: dict): return {"status": "ok" if expected == actual else "warn", "live_trading_enabled": False}

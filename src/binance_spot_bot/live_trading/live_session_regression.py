def live_session_regression(current: float, baseline: float): return {"status": "warn" if current > baseline else "ok", "regression": current - baseline, "live_trading_enabled": False}

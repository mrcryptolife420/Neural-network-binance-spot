def live_execution_quality(slippage_bps: float): return {"status": "warn" if slippage_bps > 20 else "ok", "slippage_bps": slippage_bps, "live_order_submitted": False, "live_trading_enabled": False}

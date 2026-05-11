def compute_indicator(values: list[float]): return {"status": "ok", "value": sum(values)/len(values) if values else 0, "live_trading_enabled": False}

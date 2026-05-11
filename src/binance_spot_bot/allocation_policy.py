def allocation_policy(weights: dict[str, float]): return {"status": "ok" if sum(weights.values()) <= 1.0 else "blocked", "weights": weights, "live_trading_enabled": False}

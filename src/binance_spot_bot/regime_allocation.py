def regime_allocation(regime: str): return {"regime": regime, "preset": "conservative" if regime == "volatile" else "balanced", "live_trading_enabled": False}

def strategy_rotation(scores: dict[str, float]): return {"selected": max(scores, key=scores.get) if scores else "", "live_trading_enabled": False}

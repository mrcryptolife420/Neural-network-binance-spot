def model_promotion_gate(score: float, operator_confirmed: bool): return {"status": "ok" if score >= 0.6 and operator_confirmed else "blocked", "live_trading_enabled": False}

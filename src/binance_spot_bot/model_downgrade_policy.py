def model_downgrade_policy(score: int): return {"action": "downgrade_candidate" if score <= 60 else "observe", "live_trading_enabled": False}

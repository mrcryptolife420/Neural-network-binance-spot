def rotation_governance(score: float, confirm: bool): return {"status": "approved" if score >= 0.6 and confirm else "blocked", "live_trading_enabled": False}

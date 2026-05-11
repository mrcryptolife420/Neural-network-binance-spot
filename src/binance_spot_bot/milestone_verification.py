def milestone_verification(checks: list[dict]): return {"status": "ok" if all(c.get("status") == "ok" for c in checks) else "blocked", "live_trading_enabled": False}

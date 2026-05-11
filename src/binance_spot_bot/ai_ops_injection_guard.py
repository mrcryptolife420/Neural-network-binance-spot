def injection_guard(text: str): return {"status": "blocked" if "ignore previous" in text.lower() else "ok", "live_trading_enabled": False}

def slow_check_hardening(seconds: float): return {"status": "ok" if seconds < 180 else "warn", "seconds": seconds, "live_trading_enabled": False}

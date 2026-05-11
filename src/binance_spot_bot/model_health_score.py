def model_health_score(drift: float, performance_ok: bool): return {"status": "ok" if drift <= 0.2 and performance_ok else "warn", "score": max(0, 100-int(drift*100)), "live_trading_enabled": False}

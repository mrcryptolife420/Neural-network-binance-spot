def model_monitoring_alerts(score: int): return {"status": "ok" if score >= 80 else "warn", "alerts": [] if score >= 80 else ["model_health_low"], "live_trading_enabled": False}

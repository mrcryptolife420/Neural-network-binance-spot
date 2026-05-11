def paper_os_readiness_score(checks: list[dict]): return {"score": sum(1 for c in checks if c.get("status") == "ok"), "live_trading_enabled": False}

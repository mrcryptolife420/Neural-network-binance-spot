def performance_attribution(rows: list[dict]): return {"status": "ok", "pnl": sum(float(r.get("pnl", 0)) for r in rows), "live_trading_enabled": False}

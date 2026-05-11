def post_trade_forensics(events: list[dict]): return {"status": "ok" if events else "warn", "events": len(events), "live_trading_enabled": False}

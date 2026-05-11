def evidence_interpreter(items: list[str]): return {"status": "ok" if items else "warn", "items": items, "live_trading_enabled": False}

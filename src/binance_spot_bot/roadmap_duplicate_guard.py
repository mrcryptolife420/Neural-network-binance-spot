def roadmap_duplicate_guard(names: list[str]): return {"status": "ok" if len(names) == len(set(names)) else "blocked", "live_trading_enabled": False}

def enforce_snapshot_limits(snapshot: dict, max_items: int = 100): return {"status": "ok", "limited": dict(list(snapshot.items())[:max_items]), "live_trading_enabled": False}

def data_quality_v2(rows: list[dict]): return {"status": "ok" if rows else "warn", "rows": len(rows), "live_trading_enabled": False}

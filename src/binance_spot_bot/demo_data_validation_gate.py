def demo_data_validation_gate(rows: int, quality_ok: bool): return {"status": "ok" if rows > 0 and quality_ok else "blocked", "rows": rows, "live_trading_enabled": False}

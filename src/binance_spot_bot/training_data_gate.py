def training_data_gate(rows: int, leakage_pass: bool): return {"status": "ok" if rows > 0 and leakage_pass else "blocked", "live_trading_enabled": False}

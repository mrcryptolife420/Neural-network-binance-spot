def validate_roadmap_text(text: str): return {"status": "ok" if "Definition of Done" in text else "warn", "live_trading_enabled": False}

def roadmap_quality_score(text: str): return {"status": "ok", "score": min(100, text.count("[") + text.count("##")), "live_trading_enabled": False}

def inference_compatibility(feature_hash: str, model_hash: str): return {"status": "ok" if feature_hash == model_hash else "blocked", "live_trading_enabled": False}

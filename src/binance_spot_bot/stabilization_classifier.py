def stabilization_classifier(item: str): return {"class": "blocker" if "fail" in item.lower() else "task", "live_trading_enabled": False}

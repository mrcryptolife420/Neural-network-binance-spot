def operator_signoff(confirm: str): return {"status": "signed" if confirm == "PAPER_OS_SIGNOFF" else "blocked", "live_trading_enabled": False}

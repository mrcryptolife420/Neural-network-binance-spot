def separation_of_duties(requester: str, approver: str): return {"status": "ok" if requester != approver else "blocked", "live_trading_enabled": False}

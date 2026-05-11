def risk_preset_proposal(kind: str): return {"status": "proposal", "kind": kind, "mutates_active_profile": False, "approval_required": "increase" in kind, "live_trading_enabled": False}

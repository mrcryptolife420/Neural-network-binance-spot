def stabilization_gate(blockers: list[str], waivers: list[str]): return {"status": "ok" if not (set(blockers)-set(waivers)) else "blocked", "live_trading_enabled": False}

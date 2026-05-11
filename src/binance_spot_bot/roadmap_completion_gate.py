def roadmap_completion_gate(tests_ok: bool, evidence_present: bool): return {"status": "ok" if tests_ok and evidence_present else "blocked", "live_trading_enabled": False}

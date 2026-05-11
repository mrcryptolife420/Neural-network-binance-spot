def migration_apply(name: str, confirm: str): return {"status": "blocked" if confirm != "APPLY_LOCAL_MIGRATION" else "applied", "name": name, "live_trading_enabled": False}

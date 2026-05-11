from pathlib import Path
def pre_upgrade_backup_gate(backup: Path): return {"status": "ok" if backup.exists() else "blocked", "live_trading_enabled": False}

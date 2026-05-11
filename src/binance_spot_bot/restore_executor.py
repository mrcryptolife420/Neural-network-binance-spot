from pathlib import Path
def restore_execute(zip_path: Path, target: Path, confirm: str): return {"status": "blocked" if confirm != "RESTORE_OFFLINE_STATE" else "preview_required", "zip": str(zip_path), "target": str(target), "live_trading_enabled": False}

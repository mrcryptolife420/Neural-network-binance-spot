from pathlib import Path
def data_dir_migration_preview(source: Path, target: Path): return {"status": "ready", "source": str(source), "target": str(target), "preview_only": True, "live_trading_enabled": False}

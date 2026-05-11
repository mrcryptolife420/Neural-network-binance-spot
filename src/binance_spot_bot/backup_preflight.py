from pathlib import Path
from .local_paper_os_facade import inventory
def backup_preflight(root: Path): return {"status": "ok", "inventory": inventory(root), "live_trading_enabled": False}

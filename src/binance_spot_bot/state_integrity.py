from pathlib import Path
from .local_paper_os_facade import inventory
def state_integrity_check(root: Path): return inventory(root)

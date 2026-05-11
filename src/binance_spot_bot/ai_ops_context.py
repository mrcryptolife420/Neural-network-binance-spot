from pathlib import Path
from .local_paper_os_facade import inventory
def build_ai_ops_context(root: Path): return inventory(root)

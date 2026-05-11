from pathlib import Path
from .local_paper_os_facade import restore_preview
def restore_drill(zip_path: Path, target: Path): return {**restore_preview(zip_path, target), "drill": True}

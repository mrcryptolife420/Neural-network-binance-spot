from pathlib import Path
from .local_paper_os_facade import copy_bundle
def export_compliance_bundle(files: list[Path], out: Path): return copy_bundle(files, out)

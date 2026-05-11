from pathlib import Path
from .dev_quality_facade import write_dev_report
def write_rotation_journal(root: Path, payload: dict): return write_dev_report(root, "rotation-journal", payload)

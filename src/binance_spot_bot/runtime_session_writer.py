from pathlib import Path
from .dev_quality_facade import write_dev_report
def write_runtime_session(root: Path, payload: dict): return write_dev_report(root, "runtime-session", payload)

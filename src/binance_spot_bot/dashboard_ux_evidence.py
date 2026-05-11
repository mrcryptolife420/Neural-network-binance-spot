from pathlib import Path
from .dev_quality_facade import write_dev_report
def write_dashboard_ux_evidence(root: Path, payload: dict): return write_dev_report(root, "dashboard-ux-evidence", payload)

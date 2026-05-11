from pathlib import Path
from .local_paper_os_facade import safe_record, write_json_report
def write_scheduled_report(root: Path, name: str, payload: dict): return write_json_report(root, "scheduled-reports", name, safe_record("scheduled_report", payload))

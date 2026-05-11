from pathlib import Path
from .local_paper_os_facade import safe_record, write_json_report
def write_action_center_report(root: Path, payload: dict): return write_json_report(root, "action-center", "action-center-report", safe_record("action_center_report", payload))

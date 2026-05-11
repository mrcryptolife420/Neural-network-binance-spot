from pathlib import Path
from .local_paper_os_facade import safe_record, write_json_report
def write_disaster_recovery_report(root: Path, payload: dict): return write_json_report(root, "disaster-recovery", "disaster-recovery-report", safe_record("dr_report", payload))

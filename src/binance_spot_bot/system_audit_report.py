from pathlib import Path
from .model_ops_facade import write_model_ops_report
def write_system_audit_report(root: Path, payload: dict): return write_model_ops_report(root, "system-audit-report", payload)

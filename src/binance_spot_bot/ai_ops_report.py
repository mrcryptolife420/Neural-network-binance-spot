from pathlib import Path
from .local_paper_os_facade import safe_record, write_json_report
def write_ai_ops_report(root: Path, payload: dict): return write_json_report(root, "ai-ops", "assistant-report", safe_record("ai_ops_report", payload))

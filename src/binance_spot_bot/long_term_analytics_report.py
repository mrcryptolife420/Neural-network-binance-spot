from pathlib import Path
from .local_paper_os_facade import safe_record, write_json_report
def write_long_term_analytics_report(root: Path, payload: dict): return write_json_report(root, "analytics", "long-term-analytics", safe_record("long_term_analytics", payload))

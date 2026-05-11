from pathlib import Path
from .local_paper_os_facade import safe_record, write_json_report
def write_approval_queue(root: Path, proposals: list[dict]): return write_json_report(root, "approval-queue", "latest-queue", safe_record("approval_queue", {"proposals": proposals}))

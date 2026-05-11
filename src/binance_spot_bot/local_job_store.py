from pathlib import Path
from .local_paper_os_facade import safe_record, write_json_report
def save_local_job_run(root: Path, payload: dict): return write_json_report(root, "local-jobs", "latest-run", safe_record("local_job_run", payload))

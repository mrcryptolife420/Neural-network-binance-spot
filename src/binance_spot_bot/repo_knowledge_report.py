from pathlib import Path
from .dev_quality_facade import write_dev_report
def write_repo_knowledge_report(root: Path, payload: dict): return write_dev_report(root, "repo-knowledge-report", payload)

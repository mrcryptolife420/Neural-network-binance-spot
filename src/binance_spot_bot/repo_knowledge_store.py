from pathlib import Path
from .dev_quality_facade import write_dev_report
def write_repo_knowledge_store(root: Path, payload: dict): return write_dev_report(root, "repo-knowledge-store", payload)

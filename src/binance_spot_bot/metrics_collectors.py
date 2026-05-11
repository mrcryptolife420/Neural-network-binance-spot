from .local_paper_os_facade import safe_record
def collect_artifact_metrics(items: list[dict]): return safe_record("artifact_metrics", {"artifact_count": len(items)})

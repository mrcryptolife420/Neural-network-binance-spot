from .local_paper_os_facade import safe_record
def local_ops_metric_snapshot(jobs: list[dict]): return safe_record("local_ops_metrics", {"jobs": len(jobs)})

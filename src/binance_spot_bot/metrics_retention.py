from .local_paper_os_facade import safe_record
def metrics_retention_plan(rows: list[dict], keep_latest: int = 1000): return safe_record("metrics_retention", {"keep": min(len(rows), keep_latest), "archive": max(0, len(rows)-keep_latest)})

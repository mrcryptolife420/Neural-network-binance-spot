from .local_paper_os_facade import safe_record
def due_jobs(jobs: list[dict], now_ms: int): return safe_record("due_jobs", {"jobs": [job for job in jobs if int(job.get("next_due_ms", 0)) <= now_ms]})

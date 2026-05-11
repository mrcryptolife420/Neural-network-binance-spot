from .local_paper_os_facade import safe_record
def paper_ops_calendar(jobs: list[dict]): return safe_record("paper_ops_calendar", {"jobs": jobs})

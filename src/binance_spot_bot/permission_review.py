from .local_paper_os_facade import safe_record
def permission_review(rows: list[dict]): return safe_record("permission_review", {"items": len(rows), "status": "review_required" if rows else "ok"})

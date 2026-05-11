from .local_paper_os_facade import safe_record
def record_ai_ops_feedback(rating: int, note: str = ""): return safe_record("ai_ops_feedback", {"rating": rating, "note": note})

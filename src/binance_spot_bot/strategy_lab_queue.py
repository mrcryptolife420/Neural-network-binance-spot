from .local_paper_os_facade import safe_record
def strategy_lab_queue(candidates: list[str]): return safe_record("strategy_lab_queue", {"candidates": candidates, "paper_only": True})

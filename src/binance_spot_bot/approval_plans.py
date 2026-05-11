from .local_paper_os_facade import safe_record
def approval_plan(actions: list[str]): return safe_record("approval_plan", {"actions": actions, "requires_separation_of_duties": True})

from .local_paper_os_facade import safe_record
def permission_change_workflow(role: str, change: str): return safe_record("permission_change", {"role": role, "change": change, "requires_approval": True})

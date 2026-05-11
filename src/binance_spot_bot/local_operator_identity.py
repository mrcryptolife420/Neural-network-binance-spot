from .local_paper_os_facade import safe_record
def local_operator_identity(name: str = "local-operator", role: str = "operator"): return safe_record("local_operator_identity", {"name": name, "role": role})

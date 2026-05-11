from .local_paper_os_facade import safe_record
def default_operator_roles(): return safe_record("operator_roles", {"roles": ["viewer", "operator", "key_manager", "admin"]})

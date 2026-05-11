from .local_paper_os_facade import safe_record
def approval_policy_templates(): return safe_record("approval_policy_templates", {"templates": ["single-operator-safe-action", "two-person-key-change"]})

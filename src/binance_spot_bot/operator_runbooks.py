from .local_paper_os_facade import safe_record
def runbook_index(): return safe_record("runbook_index", {"runbooks": ["daily-ops", "incident-response", "backup-restore"]})

from .local_paper_os_facade import FORBIDDEN_SUFFIXES, safe_record
def backup_profiles(): return safe_record("backup_profiles", {"profiles": ["minimal_ops", "paper_ops_full", "audit_evidence", "restore_drill_fixture"], "forbidden_suffixes": sorted(FORBIDDEN_SUFFIXES)})

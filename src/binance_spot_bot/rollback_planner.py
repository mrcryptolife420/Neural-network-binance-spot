from .dev_quality_facade import safe_record
def rollback_plan(version: str): return safe_record("rollback_plan", {"target_version": version, "requires_backup": True})

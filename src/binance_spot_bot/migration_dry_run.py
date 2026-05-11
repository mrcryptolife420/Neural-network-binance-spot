from .dev_quality_facade import safe_record
def migration_dry_run(name: str): return safe_record("migration_dry_run", {"name": name, "dry_run": True})

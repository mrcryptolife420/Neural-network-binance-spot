from .dev_quality_facade import safe_record
def migration_registry(): return safe_record("migration_registry", {"migrations": []})

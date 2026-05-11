from .dev_quality_facade import safe_record
def release_notes(version: str, changes: list[str]): return safe_record("release_notes", {"version": version, "changes": changes})

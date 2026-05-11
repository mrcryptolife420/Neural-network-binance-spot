from .dev_quality_facade import safe_record
def release_candidate(version: str): return safe_record("release_candidate", {"version": version, "status": "candidate"})

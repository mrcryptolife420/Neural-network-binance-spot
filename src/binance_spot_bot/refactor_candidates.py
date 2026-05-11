from .dev_quality_facade import safe_record
def refactor_candidates(files: list[str]): return safe_record("refactor_candidates", {"files": files[:10]})

from .dev_quality_facade import safe_record
def safety_surface_map(files: list[str]): return safe_record("safety_surface_map", {"files": files, "live_controls": []})

from .dev_quality_facade import safe_record
def dashboard_surface_map(pages: list[str]): return safe_record("dashboard_surface_map", {"pages": pages})

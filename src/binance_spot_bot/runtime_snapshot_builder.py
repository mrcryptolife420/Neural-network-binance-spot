from .dev_quality_facade import safe_record
def build_runtime_snapshot(parts: dict): return safe_record("runtime_snapshot", parts)

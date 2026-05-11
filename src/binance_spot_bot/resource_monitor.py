from .dev_quality_facade import safe_record
def resource_snapshot(cpu_pct: float = 0, memory_mb: float = 0): return safe_record("resource_snapshot", {"cpu_pct": cpu_pct, "memory_mb": memory_mb})

from .dev_quality_facade import profile_payload
def data_performance(rows: int, elapsed_ms: float): return profile_payload("data", elapsed_ms, budget_ms=max(100, rows))

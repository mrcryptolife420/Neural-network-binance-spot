from .dev_quality_facade import safe_record
def test_runtime_history(rows: list[dict]): return safe_record("test_runtime_history", {"runs": len(rows)})

from .dev_quality_facade import safe_record
def release_quality_gate(results: list[dict]): return safe_record("release_quality_gate", {"status": "ok" if all(r.get("status") == "ok" for r in results) else "blocked"})

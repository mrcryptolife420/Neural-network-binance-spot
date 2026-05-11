from .dev_quality_facade import safe_record
def flaky_tests(history: list[dict]): return safe_record("flaky_tests", {"flaky": []})

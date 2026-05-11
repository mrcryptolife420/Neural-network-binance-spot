from .dev_quality_facade import safe_record
def performance_recommendations(report: dict): return safe_record("performance_recommendations", {"recommendations": ["cache heavy reads"] if report.get("status") == "warn" else []})

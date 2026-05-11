from .dev_quality_facade import safe_record
def post_upgrade_validation(): return safe_record("post_upgrade_validation", {"checks": ["compile", "tests", "dashboard-smoke"]})

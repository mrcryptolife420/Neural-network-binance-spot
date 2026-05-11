from .dev_quality_facade import safe_record
def test_profiles(): return safe_record("test_profiles", {"profiles": ["fast", "standard", "deep"]})

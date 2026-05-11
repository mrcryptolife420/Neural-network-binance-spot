from .dev_quality_facade import profile_payload
def runtime_profile(elapsed_ms: float): return profile_payload("runtime", elapsed_ms)

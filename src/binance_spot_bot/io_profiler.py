from .dev_quality_facade import profile_payload
def io_profile(reads: int, writes: int): return profile_payload("io", reads + writes)

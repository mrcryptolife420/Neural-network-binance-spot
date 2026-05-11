from .dev_quality_facade import profile_payload
def cli_profile(command: str, elapsed_ms: float): return profile_payload(f"cli:{command}", elapsed_ms)

from .dev_quality_facade import runtime_event
def runtime_state(status: str): return runtime_event("state", {"status": status})

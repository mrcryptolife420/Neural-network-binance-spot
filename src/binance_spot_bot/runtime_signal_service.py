from .dev_quality_facade import runtime_event
def runtime_signal_service(signal: str): return runtime_event("signal_service", {"signal": signal})

from .dev_quality_facade import runtime_event
def runtime_demo_pilot_service(preset: str): return runtime_event("demo_pilot_service", {"preset": preset})

from .dev_quality_facade import runtime_event
def runtime_pipeline_step(name: str): return runtime_event("pipeline_step", {"name": name})

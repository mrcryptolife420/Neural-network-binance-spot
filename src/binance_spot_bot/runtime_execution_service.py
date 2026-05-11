from .dev_quality_facade import runtime_event
def runtime_execution_service(intent: dict): return runtime_event("execution_service", {"intent": intent, "paper_only": True})

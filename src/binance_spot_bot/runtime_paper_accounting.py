from .dev_quality_facade import runtime_event
def runtime_paper_accounting(equity: str): return runtime_event("paper_accounting", {"equity": equity})

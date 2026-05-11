from .model_ops_facade import stabilization_status
def stabilization_workplan(blockers: list[str]): return stabilization_status(blockers)

from .model_ops_facade import stabilization_status
def stabilization_audit_ingest(blockers: list[str]): return stabilization_status(blockers)

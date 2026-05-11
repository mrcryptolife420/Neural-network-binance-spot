from .local_paper_os_facade import safe_record
def evaluate_ops_slo(metrics: dict): return safe_record("ops_slo", {"status": "ok", **metrics})

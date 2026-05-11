from .local_paper_os_facade import safe_record
def governance_metric_snapshot(decisions: list[dict]): return safe_record("governance_metrics", {"decisions": len(decisions)})

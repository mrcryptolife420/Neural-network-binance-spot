from .local_paper_os_facade import safe_record
def decision_outcome_analytics(decisions: list[dict]): return safe_record("decision_outcomes", {"decisions": len(decisions), "approved": sum(1 for d in decisions if d.get("approved"))})

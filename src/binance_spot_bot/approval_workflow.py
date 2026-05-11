from .action_center import propose_action, review_action
def approval_workflow(action_type: str, approved: bool = False): return review_action(propose_action(action_type, "workflow"), approved=approved)

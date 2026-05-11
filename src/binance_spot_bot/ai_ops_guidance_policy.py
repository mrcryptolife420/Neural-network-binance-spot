from .local_paper_os_facade import safe_record
def guidance_policy(action: str): return safe_record("ai_ops_guidance_policy", {"action": action, "allowed": action in {"explain", "summarize", "propose_command"}})

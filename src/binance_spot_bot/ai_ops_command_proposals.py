from .local_paper_os_facade import is_safe_command, safe_record
def propose_ai_ops_command(command: str): return safe_record("ai_ops_command_proposal", {"command": command, "allowed": is_safe_command(command)})

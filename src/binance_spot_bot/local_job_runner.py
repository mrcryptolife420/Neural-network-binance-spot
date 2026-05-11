from .local_paper_os_facade import is_safe_command, safe_record
def run_local_job(command: str): return safe_record("local_job_result", {"command": command, "allowed": is_safe_command(command)}, status="ready" if is_safe_command(command) else "blocked")

from .local_paper_os_facade import is_safe_command, safe_record
def windows_task_plan(command: str, name: str = "SpotBotLocalOps"): return safe_record("windows_task_plan", {"name": name, "command": command, "allowed": is_safe_command(command)})

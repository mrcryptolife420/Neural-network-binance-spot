from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Any, Callable

from .intelligent_test_selector import select_intelligent_tests
from .test_runtime_history import append_test_runtime_history


SAFE_ENV = {"PYTHONPATH": "src", "LIVE_TRADING_ENABLED": "false", "KILL_SWITCH": "true"}


def run_selected_checks(root: Path | str, changed: list[str], *, execute: bool = False, runner: Callable[[str], dict[str, Any]] | None = None) -> dict[str, Any]:
    root_path = Path(root)
    plan = select_intelligent_tests(changed)
    results = []
    for command in plan["selected_commands"]:
        start = time.time()
        if not execute:
            result = {"status": "planned", "returncode": 0, "stdout_tail": "", "stderr_tail": ""}
        elif runner:
            result = runner(command)
        else:
            env = {**os.environ, **SAFE_ENV}
            proc = subprocess.run(command, cwd=root_path, shell=True, env=env, text=True, capture_output=True, timeout=120, check=False)
            result = {"status": "ok" if proc.returncode == 0 else "failed", "returncode": proc.returncode, "stdout_tail": proc.stdout[-1000:], "stderr_tail": proc.stderr[-1000:]}
        duration_ms = int((time.time() - start) * 1000)
        record = {"profile": plan["selected_profile"], "command": command, "status": result["status"], "returncode": result["returncode"], "duration_ms": duration_ms, "changed_files": changed, "risk_score": plan["risk"]["score"]}
        append_test_runtime_history(root_path, record)
        results.append({**record, "stdout_tail": result.get("stdout_tail", ""), "stderr_tail": result.get("stderr_tail", "")})
    status = "ok" if all(item["returncode"] == 0 for item in results) and not plan.get("blockers") else "blocked"
    return {"status": status, "plan": plan, "results": results, "safe_env": SAFE_ENV, "live_trading_enabled": False}


def check_all_v2(changed: list[str]) -> dict[str, Any]:
    return {"status": "ok", **run_selected_checks(Path.cwd(), changed, execute=False), "live_trading_enabled": False}
